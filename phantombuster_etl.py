#!/usr/bin/env python3
"""
PhantomBuster -> Notion ETL Pipeline
Syncs LinkedIn engagement leads from PhantomBuster into the Grove Community Engagement Hub.

Databases:
  - Contacts: People who engaged with Jim's content
  - Engagements: Individual like/comment events linked to Contacts and Posts
  - Posts: Jim's LinkedIn posts that generated engagement

Usage:
    python phantombuster_etl.py              # Full sync
    python phantombuster_etl.py --dry-run    # Preview without writing to Notion
    python phantombuster_etl.py --stats      # Show sync stats only
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
NOTION_KEY = os.environ.get('NOTION_API_KEY', '')
PB_API_KEY = os.environ.get('PHANTOMBUSTER_API_KEY', ''')

# Notion database IDs
CONTACTS_DB = '08b9f73264b24e4b82d4c842f5a11cc8'
ENGAGEMENTS_DB = '25e138b54d1645a3a78b266451585de9'
POSTS_DB = '46448a0166ce42d1bdadc69cad0c7576'

# PhantomBuster agent configs — agent_id: s3_folder
PB_AGENTS = {
    '5464281464072346': 'jtS7HbSonE1KJQH2XbGQyQ',  # Master: Commenter & Liker Scraper
    '7681394493723575': 'Nd6Y4mRgYhJAk7FDqRLlww',  # Likers Export
    '589974210280169':  '8qohyJcD21I9aXuPlftiLA',  # Commenters Export
    '1194668210811742': 'OSfw84VqJ92HoMMcJGtdSw',  # Profile Scraper
}
PB_S3_BASE = 'https://phantombuster.s3.amazonaws.com/fPnqqqrVtDA'

REQUEST_TIMEOUT = 20
SYNC_STATE_FILE = Path(__file__).parent / '.pb_sync_state.json'

NOTION_HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# --- Degree mapping ---
DEGREE_MAP = {
    '1st': '1st',
    '2nd': '2nd',
    '3rd': '3rd+',
    '3rd+': '3rd+',
    'Following': 'Following',
}

# --- Contact Classification ---
# Keyword sets for Sector classification (checked against lowercase headline)
SECTOR_KEYWORDS = {
    'AI/ML Specialist': [
        'artificial intelligence', ' ai ', 'machine learning', 'deep learning',
        'nlp', 'llm', 'large language', 'neural', 'computer vision', 'data scientist',
        'ml engineer', 'ai engineer', 'ai researcher', 'generative ai', 'gpt',
        'transformer', 'reinforcement learning', 'ai/ml', 'ai &', '& ai',
    ],
    'Academia': [
        'professor', ' phd', 'researcher', 'university', 'academic', 'postdoc',
        'faculty', 'graduate student', 'doctoral', 'lecturer', 'adjunct',
        'research fellow', 'lab director', 'dean', 'provost',
    ],
    'Investor': [
        'venture capital', 'investor', 'angel investor', 'partner at', 'fund manager',
        'vc ', ' vc', 'capital', 'portfolio', 'limited partner', 'seed',
        'series a', 'series b', 'venture partner',
    ],
    'Influencer': [
        'thought leader', 'speaker', 'keynote', 'author of', 'podcast',
        'content creator', 'influencer', 'evangelist', 'community builder',
        'newsletter', 'youtuber', 'creator economy',
    ],
    'Job Seeker': [
        'seeking', 'looking for', 'open to work', 'job search', 'available for',
        'actively looking', 'career transition', 'between roles',
    ],
    'Corporate': [
        'vp ', 'vice president', 'director of', 'head of', 'chief',
        'ceo', 'cfo', 'coo', 'cio', 'cto', 'enterprise', 'manager at',
        'senior director', 'svp', 'evp', 'general manager',
    ],
    'Tech': [
        'software', 'developer', 'engineer', 'devops', 'cloud', 'saas',
        'platform', 'startup', 'full stack', 'frontend', 'backend',
        'architect', 'infrastructure', 'systems', 'open source',
        'distributed', 'blockchain', 'web3', 'product manager', 'tech lead',
    ],
}

# Grove-aligned keywords for alignment scoring (headline + comment content)
GROVE_STRONG_KEYWORDS = [
    'distributed', 'decentraliz', 'edge computing', 'peer-to-peer', 'p2p',
    'local-first', 'knowledge graph', 'collective intelligence', 'cognitive',
    'open source ai', 'federated', 'hybrid intelligence', 'autonomous agent',
    'multi-agent', 'knowledge commons', 'infrastructure', 'self-sovereign',
    'exploration', 'declarative', 'ai village', 'personal ai',
]
GROVE_MODERATE_KEYWORDS = [
    'ai agent', 'llm', 'language model', 'open source', 'privacy',
    'developer tool', 'local ai', 'on-device', 'ai infrastructure',
    'knowledge management', 'second brain', 'personal knowledge',
    'ai assistant', 'copilot', 'rag', 'retrieval', 'embedding',
]

# Strategic bucket keyword signals
BUCKET_GOVERNANCE_KEYWORDS = [
    'policy', 'governance', 'ethics', 'regulation', 'compliance', 'legal',
    'responsible ai', 'ai safety', 'alignment', 'trust', 'fairness',
]
BUCKET_SENIOR_TITLES = [
    'ceo', 'cfo', 'coo', 'cto', 'cio', 'vp ', 'vice president', 'svp',
    'evp', 'director', 'partner', 'founder', 'co-founder', 'head of',
    'chief', 'general manager', 'managing director',
]


def classify_sector(headline: str) -> str:
    """Classify contact into a Sector based on headline keywords."""
    hl = f' {headline.lower()} '
    # Check in priority order (AI/ML first, then specialized, then general)
    for sector in ['AI/ML Specialist', 'Academia', 'Investor', 'Influencer',
                    'Job Seeker', 'Corporate', 'Tech']:
        for kw in SECTOR_KEYWORDS[sector]:
            if kw in hl:
                return sector
    return 'Other'


def classify_grove_alignment(headline: str, comment_text: str = '',
                              has_commented: bool = False, has_liked: bool = False) -> str:
    """Score Grove alignment from 1-5 stars based on headline + engagement signals."""
    hl = f' {headline.lower()} '
    ct = f' {comment_text.lower()} ' if comment_text else ''
    combined = hl + ct

    score = 0
    # Strong keyword matches
    for kw in GROVE_STRONG_KEYWORDS:
        if kw in combined:
            score += 3
    # Moderate keyword matches
    for kw in GROVE_MODERATE_KEYWORDS:
        if kw in combined:
            score += 1
    # Engagement bonuses
    if has_commented and len(comment_text) > 50:
        score += 2  # Substantive commenter
    elif has_commented:
        score += 1
    if has_liked:
        score += 0.5

    if score >= 8:
        return '\u2b50\u2b50\u2b50\u2b50\u2b50 Strong Thesis Alignment'
    elif score >= 5:
        return '\u2b50\u2b50\u2b50\u2b50 Good Alignment'
    elif score >= 3:
        return '\u2b50\u2b50\u2b50 Moderate Interest'
    elif score >= 1:
        return '\u2b50\u2b50 Peripheral Interest'
    else:
        return '\u2b50 Minimal Alignment'


def classify_strategic_buckets(headline: str, sector: str) -> List[str]:
    """Assign zero or more Strategic Buckets based on sector + headline signals."""
    hl = f' {headline.lower()} '
    buckets = []

    if sector == 'Academia':
        buckets.append('University Pipeline')
    if sector in ('AI/ML Specialist', 'Tech'):
        for kw in ['open source', 'contributor', 'maintainer', 'developer', 'engineer',
                    'architect', 'infrastructure', 'distributed', 'systems']:
            if kw in hl:
                buckets.append('Technical Contributors')
                break
    if sector == 'Influencer' or sector == 'Corporate':
        # Check for senior influence
        for kw in BUCKET_SENIOR_TITLES:
            if kw in hl:
                buckets.append('Content Amplifiers')
                break
        if sector == 'Influencer' and 'Content Amplifiers' not in buckets:
            buckets.append('Content Amplifiers')
    for kw in BUCKET_GOVERNANCE_KEYWORDS:
        if kw in hl:
            buckets.append('Governance/Policy')
            break
    # Potential Advisors: senior people with relevant backgrounds
    for kw in BUCKET_SENIOR_TITLES:
        if kw in hl:
            for akw in ['ai', 'infrastructure', 'platform', 'distributed', 'open source',
                         'venture', 'investor', 'research']:
                if akw in hl:
                    if 'Potential Advisors' not in buckets:
                        buckets.append('Potential Advisors')
                    break
            break
    if sector == 'Corporate':
        for kw in ['enterprise', 'saas', 'b2b', 'platform', 'digital transformation']:
            if kw in hl:
                buckets.append('Enterprise Clients')
                break

    return list(dict.fromkeys(buckets))  # dedupe preserving order


def classify_priority(alignment: str, has_commented: bool, comment_text: str = '') -> str:
    """Assign Priority based on alignment + engagement depth."""
    is_strong = 'Strong' in alignment or 'Good' in alignment
    is_substantive = has_commented and len(comment_text) > 50

    if is_strong and is_substantive:
        return 'High'
    elif is_strong or is_substantive:
        return 'Medium'
    elif 'Moderate' in alignment:
        return 'Standard'
    else:
        return 'Low'


def classify_sales_nav_status(sector: str, buckets: List[str]) -> str:
    """Derive Sales Nav List Status from sector and strategic buckets."""
    if 'University Pipeline' in buckets:
        return 'Saved - Academic'
    if 'Enterprise Clients' in buckets:
        return 'Saved - Enterprise'
    if sector in ('AI/ML Specialist', 'Tech') or 'Technical Contributors' in buckets:
        return 'Saved - Technical'
    if sector == 'Influencer' or 'Content Amplifiers' in buckets:
        return 'Saved - Influencer'
    return 'Not Saved'


def classify_contact(lead: Dict) -> Dict:
    """Run full classification pipeline on a lead. Returns dict of Notion property values."""
    headline = lead.get('occupation', '')
    comment_text = lead.get('comments', '')
    has_commented = lead.get('hasCommented') == 'true'
    has_liked = lead.get('hasLiked') == 'true'

    sector = classify_sector(headline)
    alignment = classify_grove_alignment(headline, comment_text, has_commented, has_liked)
    buckets = classify_strategic_buckets(headline, sector)
    priority = classify_priority(alignment, has_commented, comment_text)
    sales_nav = classify_sales_nav_status(sector, buckets)

    return {
        'sector': sector,
        'alignment': alignment,
        'buckets': buckets,
        'priority': priority,
        'sales_nav': sales_nav,
    }


# --- Sync state ---
def load_sync_state() -> Dict:
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text())
    return {'synced_contacts': {}, 'synced_engagements': {}, 'synced_posts': {}, 'last_sync': None}


def save_sync_state(state: Dict):
    state['last_sync'] = datetime.now(timezone.utc).isoformat()
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2))


# --- PhantomBuster data fetching ---
def fetch_pb_results(agent_id: str) -> List[Dict]:
    """Fetch result.json from a PhantomBuster agent's S3 output."""
    s3_folder = PB_AGENTS.get(agent_id)
    if not s3_folder:
        print(f"  WARN: Unknown agent {agent_id}")
        return []

    url = f'{PB_S3_BASE}/{s3_folder}/result.json'
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            return resp.json()
        print(f"  WARN: S3 fetch failed ({resp.status_code}): {url}")
    except Exception as e:
        print(f"  WARN: S3 fetch error: {e}")
    return []


def fetch_all_pb_leads() -> List[Dict]:
    """Fetch and merge leads from all configured agents, dedup by memberId."""
    all_leads = {}
    for agent_id, folder in PB_AGENTS.items():
        leads = fetch_pb_results(agent_id)
        print(f"  Agent {agent_id}: {len(leads)} leads")
        for lead in leads:
            mid = lead.get('memberId', '')
            if mid and mid not in all_leads:
                all_leads[mid] = lead
            elif mid and mid in all_leads:
                # Merge — keep the record with more data
                existing = all_leads[mid]
                if lead.get('comments') and not existing.get('comments'):
                    all_leads[mid] = lead
    return list(all_leads.values())


# --- Notion helpers ---
def notion_post(url: str, payload: dict) -> Optional[requests.Response]:
    try:
        return requests.post(url, headers=NOTION_HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print(f"  WARN: Notion POST failed: {e}")
        return None


def notion_patch(url: str, payload: dict) -> Optional[requests.Response]:
    try:
        return requests.patch(url, headers=NOTION_HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print(f"  WARN: Notion PATCH failed: {e}")
        return None


def query_notion_db(db_id: str, filter_payload: dict) -> List[Dict]:
    """Query a Notion database with a filter, return all matching pages."""
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    resp = notion_post(url, {"filter": filter_payload})
    if resp and resp.status_code == 200:
        return resp.json().get('results', [])
    return []


def find_contact_by_member_id(member_id: str) -> Optional[Dict]:
    """Find existing contact by PhantomBuster memberId stored in Notes as 'PB:XXXXX'.

    This is the PRIMARY dedup key — LinkedIn users can have multiple vanity URLs
    but memberId is stable and unique.
    """
    results = query_notion_db(CONTACTS_DB, {
        "property": "Notes",
        "rich_text": {"starts_with": f"PB:{member_id}"}
    })
    return results[0] if results else None


def find_contact_by_linkedin_url(linkedin_url: str) -> Optional[Dict]:
    """Find existing contact by LinkedIn URL (fallback dedup)."""
    results = query_notion_db(CONTACTS_DB, {
        "property": "LinkedIn URL",
        "url": {"equals": linkedin_url}
    })
    return results[0] if results else None


def find_post_by_linkedin_url(post_url: str) -> Optional[Dict]:
    """Find existing post by LinkedIn URL."""
    results = query_notion_db(POSTS_DB, {
        "property": "LinkedIn URL",
        "url": {"equals": post_url}
    })
    return results[0] if results else None


# --- Notion upsert operations ---
def create_contact(lead: Dict) -> Optional[str]:
    """Create a Contact in Notion from a PhantomBuster lead. Returns page ID."""
    name = lead.get('fullName') or f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip()
    linkedin_url = lead.get('profileUrl') or lead.get('profileLink', '')
    headline = lead.get('occupation', '')
    degree = DEGREE_MAP.get(lead.get('degree', ''), 'Unknown')

    if not name or not linkedin_url:
        return None

    # Normalize LinkedIn URL
    if linkedin_url and not linkedin_url.endswith('/'):
        linkedin_url += '/'

    # Classify the contact
    classification = classify_contact(lead)

    payload = {
        "parent": {"database_id": CONTACTS_DB},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "LinkedIn URL": {"url": linkedin_url},
            "Headline": {"rich_text": [{"text": {"content": headline[:2000]}}]} if headline else {"rich_text": []},
            "LinkedIn Degree": {"select": {"name": degree}},
            "Relationship Stage": {"select": {"name": "Engaged"}},
            "Connection Level": {"select": {"name": degree}},
            "Sector": {"select": {"name": classification['sector']}},
            "Grove Alignment": {"select": {"name": classification['alignment']}},
            "Priority": {"select": {"name": classification['priority']}},
            "Sales Nav List Status": {"select": {"name": classification['sales_nav']}},
            "Last Active": {"date": {"start": datetime.now(timezone.utc).strftime('%Y-%m-%d')}},
        }
    }

    # Strategic Bucket is multi_select
    if classification['buckets']:
        payload["properties"]["Strategic Bucket"] = {
            "multi_select": [{"name": b} for b in classification['buckets']]
        }

    # Store memberId in Notes for dedup tracking
    member_id = lead.get('memberId', '')
    if member_id:
        payload["properties"]["Notes"] = {
            "rich_text": [{"text": {"content": f"PB:{member_id}"}}]
        }

    resp = notion_post('https://api.notion.com/v1/pages', payload)
    if resp and resp.status_code in [200, 201]:
        page_id = resp.json()['id']
        return page_id
    else:
        status = resp.status_code if resp else 'no response'
        detail = resp.text[:120] if resp else ''
        print(f"    ERROR creating contact '{name}': {status} {detail}")
        return None


def update_contact_on_new_engagement(contact_page_id: str, lead: Dict) -> bool:
    """Update an existing contact with new engagement data (longitudinal tracking).

    Called when we see a returning engager on a new post. Updates:
    - Last Active date
    - Relationship Stage (upgrade if deeper engagement)
    - Re-classify if headline changed (people update their profiles)
    """
    classification = classify_contact(lead)
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    payload = {
        "properties": {
            "Last Active": {"date": {"start": today}},
            # Re-apply classification (headline may have changed)
            "Sector": {"select": {"name": classification['sector']}},
            "Grove Alignment": {"select": {"name": classification['alignment']}},
            "Priority": {"select": {"name": classification['priority']}},
            "Sales Nav List Status": {"select": {"name": classification['sales_nav']}},
        }
    }

    if classification['buckets']:
        payload["properties"]["Strategic Bucket"] = {
            "multi_select": [{"name": b} for b in classification['buckets']]
        }

    resp = notion_patch(f'https://api.notion.com/v1/pages/{contact_page_id}', payload)
    if resp and resp.status_code == 200:
        return True
    else:
        status = resp.status_code if resp else 'no response'
        print(f"    WARN: Failed to update contact {contact_page_id}: {status}")
        return False


def create_engagement(lead: Dict, contact_page_id: str, post_page_id: str, eng_type: str) -> Optional[str]:
    """Create an Engagement in Notion. Returns page ID."""
    name = lead.get('fullName') or f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip()
    comment_text = lead.get('comments', '')

    if eng_type == 'comment':
        title = f"{name} commented"
        notion_type = "Commented on Our Post"
        their_content = comment_text
        quality = "Substantive" if len(comment_text) > 50 else "Brief"
        response_status = "Needs Reply" if quality == "Substantive" else "No Reply Needed"
    else:
        title = f"{name} liked"
        notion_type = "Liked"
        their_content = ""
        quality = "Reaction-only"
        response_status = "No Reply Needed"

    # Parse date
    date_str = lead.get('lastCommentedAt') or lead.get('timestamp', '')
    date_val = date_str[:10] if date_str else datetime.now(timezone.utc).strftime('%Y-%m-%d')

    payload = {
        "parent": {"database_id": ENGAGEMENTS_DB},
        "properties": {
            "Engagement": {"title": [{"text": {"content": title}}]},
            "Contact": {"relation": [{"id": contact_page_id}]},
            "Post": {"relation": [{"id": post_page_id}]},
            "Type": {"select": {"name": notion_type}},
            "Direction": {"select": {"name": "Inbound"}},
            "Engagement Quality": {"select": {"name": quality}},
            "Response Status": {"select": {"name": response_status}},
            "Date": {"date": {"start": date_val}},
        }
    }

    if their_content:
        payload["properties"]["Their Content"] = {
            "rich_text": [{"text": {"content": their_content[:2000]}}]
        }

    comment_url = lead.get('commentUrl', '')
    if comment_url and eng_type == 'comment':
        payload["properties"]["Their Post URL"] = {"url": comment_url}

    resp = notion_post('https://api.notion.com/v1/pages', payload)
    if resp and resp.status_code in [200, 201]:
        return resp.json()['id']
    else:
        status = resp.status_code if resp else 'no response'
        detail = resp.text[:120] if resp else ''
        print(f"    ERROR creating engagement '{title}': {status} {detail}")
        return None


def ensure_post_exists(post_url: str, post_content: str = '') -> Optional[str]:
    """Find or create a Post entry. Returns page ID."""
    existing = find_post_by_linkedin_url(post_url)
    if existing:
        return existing['id']

    # Derive a title from post content
    title = post_content[:80].split('\n')[0] if post_content else 'Untitled Post'
    if len(title) < len(post_content[:80]):
        title += '...'

    payload = {
        "parent": {"database_id": POSTS_DB},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "LinkedIn URL": {"url": post_url},
            "Status": {"select": {"name": "Published"}},
        }
    }

    resp = notion_post('https://api.notion.com/v1/pages', payload)
    if resp and resp.status_code in [200, 201]:
        return resp.json()['id']
    print(f"  ERROR creating post: {resp.status_code if resp else 'no response'}")
    return None


# --- Main ETL ---
def run_etl(dry_run: bool = False, stats_only: bool = False):
    print("=" * 60)
    print("PHANTOMBUSTER -> NOTION ETL")
    print(f"  Mode: {'DRY RUN' if dry_run else 'STATS' if stats_only else 'LIVE'}")
    print("=" * 60)

    if not NOTION_KEY:
        print("\nERROR: NOTION_API_KEY not set")
        sys.exit(1)

    state = load_sync_state()
    if state['last_sync']:
        print(f"  Last sync: {state['last_sync']}")

    # 1. Fetch leads from PhantomBuster
    print(f"\n[1/4] Fetching leads from PhantomBuster...")
    leads = fetch_all_pb_leads()
    print(f"  Total unique leads: {len(leads)}")

    if stats_only:
        commenters = sum(1 for l in leads if l.get('hasCommented') == 'true')
        likers = sum(1 for l in leads if l.get('hasLiked') == 'true')
        already_synced = sum(1 for l in leads if l.get('memberId', '') in state['synced_contacts'])
        new_leads = len(leads) - already_synced
        print(f"  Commenters: {commenters}")
        print(f"  Likers: {likers}")
        print(f"  Already synced: {already_synced}")
        print(f"  New: {new_leads}")
        # Classification breakdown
        sectors = {}
        alignments = {}
        buckets_count = {}
        for l in leads:
            c = classify_contact(l)
            sectors[c['sector']] = sectors.get(c['sector'], 0) + 1
            # Use star count for display (avoids Windows encoding issues)
            star_count = c['alignment'].count('\u2b50')
            label = f"{star_count}-star"
            alignments[label] = alignments.get(label, 0) + 1
            for b in c['buckets']:
                buckets_count[b] = buckets_count.get(b, 0) + 1
        print(f"\n  Classification Preview:")
        print(f"  Sectors: {sectors}")
        print(f"  Alignment: {alignments}")
        print(f"  Strategic Buckets: {buckets_count}")
        return

    # 2. Group by post URL
    print(f"\n[2/4] Identifying posts...")
    posts_seen = {}
    for lead in leads:
        post_url = lead.get('postsUrl', '')
        if post_url and post_url not in posts_seen:
            posts_seen[post_url] = lead.get('postContent', '')
    print(f"  Found {len(posts_seen)} unique post(s)")

    # 3. Ensure posts exist in Notion
    post_page_ids = {}
    for post_url, content in posts_seen.items():
        if post_url in state['synced_posts']:
            post_page_ids[post_url] = state['synced_posts'][post_url]
            continue
        if dry_run:
            print(f"  [DRY] Would create post: {content[:60]}...")
            post_page_ids[post_url] = 'dry-run-id'
        else:
            page_id = ensure_post_exists(post_url, content)
            if page_id:
                post_page_ids[post_url] = page_id
                state['synced_posts'][post_url] = page_id
                print(f"  Post: {content[:50]}... -> {page_id}")
            time.sleep(0.35)

    # 4. Sync contacts and engagements
    print(f"\n[3/4] Syncing contacts & engagements...")
    new_contacts = 0
    updated_contacts = 0
    new_engagements = 0
    skipped = 0
    errors = 0

    for i, lead in enumerate(leads, 1):
        member_id = lead.get('memberId', '')
        linkedin_url = lead.get('profileUrl') or lead.get('profileLink', '')
        if linkedin_url and not linkedin_url.endswith('/'):
            linkedin_url += '/'
        name = lead.get('fullName') or f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip()
        post_url = lead.get('postsUrl', '')

        if not member_id or not linkedin_url:
            skipped += 1
            continue

        if i % 20 == 0:
            print(f"  Processing lead {i}/{len(leads)}...")

        # Upsert contact
        contact_page_id = state['synced_contacts'].get(member_id)
        is_returning = contact_page_id is not None
        if not contact_page_id:
            if dry_run:
                classification = classify_contact(lead)
                stars = classification['alignment'].count('\u2b50')
                print(f"  [DRY] Would create contact: {name} | {classification['sector']} | {stars}-star alignment")
                contact_page_id = 'dry-run-id'
            else:
                # Dedup: check by memberId first (primary key), then URL (fallback)
                existing = None
                if member_id:
                    existing = find_contact_by_member_id(member_id)
                if not existing:
                    existing = find_contact_by_linkedin_url(linkedin_url)
                if existing:
                    contact_page_id = existing['id']
                    state['synced_contacts'][member_id] = contact_page_id
                    is_returning = True
                else:
                    contact_page_id = create_contact(lead)
                    if contact_page_id:
                        state['synced_contacts'][member_id] = contact_page_id
                        new_contacts += 1
                    else:
                        errors += 1
                        continue
                time.sleep(0.35)

        # Longitudinal: update existing contacts with latest classification + Last Active
        if is_returning and not dry_run:
            if update_contact_on_new_engagement(contact_page_id, lead):
                updated_contacts += 1
            time.sleep(0.35)
        elif is_returning and dry_run:
            classification = classify_contact(lead)
            stars = classification['alignment'].count('\u2b50')
            print(f"  [DRY] Would update returning contact: {name} | {classification['sector']} | {stars}-star alignment")

        # Create engagements
        post_page_id = post_page_ids.get(post_url)
        if not contact_page_id or not post_page_id:
            continue

        # Comment engagement
        has_commented = lead.get('hasCommented') == 'true'
        comment_key = f"{member_id}:comment:{post_url}"
        if has_commented and comment_key not in state['synced_engagements']:
            if dry_run:
                print(f"  [DRY] Would create engagement: {name} commented")
            else:
                eng_id = create_engagement(lead, contact_page_id, post_page_id, 'comment')
                if eng_id:
                    state['synced_engagements'][comment_key] = eng_id
                    new_engagements += 1
                else:
                    errors += 1
                time.sleep(0.35)

        # Like engagement
        has_liked = lead.get('hasLiked') == 'true'
        like_key = f"{member_id}:like:{post_url}"
        if has_liked and like_key not in state['synced_engagements']:
            if dry_run:
                print(f"  [DRY] Would create engagement: {name} liked")
            else:
                eng_id = create_engagement(lead, contact_page_id, post_page_id, 'like')
                if eng_id:
                    state['synced_engagements'][like_key] = eng_id
                    new_engagements += 1
                else:
                    errors += 1
                time.sleep(0.35)

    # Save state
    if not dry_run:
        save_sync_state(state)

    # Summary
    print(f"\n[4/4] Summary")
    print(f"  Leads processed: {len(leads)}")
    print(f"  New contacts: {new_contacts}")
    print(f"  Updated (returning): {updated_contacts}")
    print(f"  New engagements: {new_engagements}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total synced contacts: {len(state['synced_contacts'])}")
    print(f"  Total synced engagements: {len(state['synced_engagements'])}")
    print("=" * 60)


# --- Sales Navigator Export Pipeline ---
SALES_NAV_SEGMENTS = {
    'Saved - Academic': 'academic',
    'Saved - Enterprise': 'enterprise',
    'Saved - Technical': 'technical',
    'Saved - Influencer': 'influencer',
}

EXPORT_DIR = Path(__file__).parent / 'sales_nav_exports'

# Sales Nav Lead Sender phantom config
SALES_NAV_AGENT_ID = os.environ.get('PB_SALES_NAV_AGENT_ID', '7375614927727918')


def query_contacts_by_sales_nav_status(status: str) -> List[Dict]:
    """Query Notion Contacts DB for contacts with a specific Sales Nav List Status."""
    results = query_notion_db(CONTACTS_DB, {
        "property": "Sales Nav List Status",
        "select": {"equals": status}
    })
    return results


def extract_linkedin_url(page: Dict) -> str:
    """Extract LinkedIn URL from a Notion page."""
    url_prop = page.get('properties', {}).get('LinkedIn URL', {}).get('url', '')
    return url_prop or ''


def extract_contact_name(page: Dict) -> str:
    """Extract name from a Notion page."""
    title = page.get('properties', {}).get('Name', {}).get('title', [])
    return title[0].get('plain_text', '') if title else ''


def export_sales_nav_contacts():
    """Export classified contacts as segment CSVs for Sales Nav Lead Sender.

    Creates one CSV per Sales Nav segment in the sales_nav_exports/ directory.
    Each CSV has columns: profileUrl, name, sector, alignment, segment
    """
    print("=" * 60)
    print("SALES NAV EXPORT")
    print("=" * 60)

    if not NOTION_KEY:
        print("\nERROR: NOTION_API_KEY not set")
        sys.exit(1)

    EXPORT_DIR.mkdir(exist_ok=True)
    total_exported = 0
    segment_files = {}

    for status, slug in SALES_NAV_SEGMENTS.items():
        print(f"\n  Querying: {status}...")
        pages = query_contacts_by_sales_nav_status(status)
        print(f"  Found {len(pages)} contacts")

        if not pages:
            continue

        csv_path = EXPORT_DIR / f'sales_nav_{slug}.csv'
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            f.write('profileUrl,name,segment\n')
            for page in pages:
                url = extract_linkedin_url(page)
                name = extract_contact_name(page)
                if url:
                    # Escape commas in name
                    safe_name = name.replace('"', '""')
                    f.write(f'{url},"{safe_name}",{slug}\n')
                    total_exported += 1

        segment_files[slug] = csv_path
        print(f"  Exported to: {csv_path}")
        time.sleep(0.5)

    # Also create a combined CSV with all segments
    combined_path = EXPORT_DIR / 'sales_nav_all.csv'
    with open(combined_path, 'w', encoding='utf-8', newline='') as f:
        f.write('profileUrl,name,segment\n')
        for status, slug in SALES_NAV_SEGMENTS.items():
            pages = query_contacts_by_sales_nav_status(status)
            for page in pages:
                url = extract_linkedin_url(page)
                name = extract_contact_name(page)
                if url:
                    safe_name = name.replace('"', '""')
                    f.write(f'{url},"{safe_name}",{slug}\n')
            time.sleep(0.5)

    print(f"\n  Summary:")
    print(f"  Total contacts exported: {total_exported}")
    print(f"  Segments: {list(segment_files.keys())}")
    print(f"  Combined CSV: {combined_path}")
    print(f"  Individual CSVs: {EXPORT_DIR}")
    print("=" * 60)

    return segment_files


def launch_lead_sender(csv_url: str, agent_id: str = '', limit: int = 25) -> Optional[str]:
    """Launch the Sales Nav Lead Sender phantom via API.

    Merges the saved agent config (session cookie, user agent) with the
    provided spreadsheet URL. The phantom navigates each profile and saves
    it to the Sales Navigator Leads page.

    Args:
        csv_url: URL to a Google Sheet or CSV with LinkedIn profile URLs
        agent_id: PhantomBuster agent ID (falls back to SALES_NAV_AGENT_ID)
        limit: Max leads to process per launch (default 25)

    Returns:
        Container ID if launched, None on error
    """
    agent_id = agent_id or SALES_NAV_AGENT_ID
    if not agent_id:
        print("ERROR: No Sales Nav Lead Sender agent ID configured.")
        print("  Set PB_SALES_NAV_AGENT_ID env var or pass agent_id parameter.")
        return None

    headers_pb = {
        'X-Phantombuster-Key-1': PB_API_KEY,
        'Content-Type': 'application/json'
    }

    # Fetch saved config to get session cookie + user agent
    print(f"\nLaunching Sales Nav Lead Sender...")
    print(f"  Agent: {agent_id}")
    try:
        resp = requests.get(
            f'https://api.phantombuster.com/api/v2/agents/fetch?id={agent_id}',
            headers=headers_pb, timeout=15)
        saved_arg = json.loads(resp.json().get('argument', '{}'))
    except Exception as e:
        print(f"  ERROR fetching agent config: {e}")
        return None

    session_cookie = saved_arg.get('sessionCookie', '')
    user_agent = saved_arg.get('userAgent', '')
    if not session_cookie:
        print("  ERROR: No session cookie in agent config. Reconfigure in PB web UI.")
        return None

    # Build full argument (launch overrides the entire argument)
    launch_arg = {
        'sessionCookie': session_cookie,
        'userAgent': user_agent,
        'spreadsheetUrl': csv_url,
        'anyLeadProfileUrlsColumnName': 'profileUrl',
        'numberOfAddsPerLaunch': limit,
    }

    print(f"  Input: {csv_url}")
    print(f"  Limit: {limit} leads")

    try:
        resp = requests.post(
            'https://api.phantombuster.com/api/v2/agents/launch',
            headers=headers_pb,
            json={'id': agent_id, 'argument': json.dumps(launch_arg)},
            timeout=120)
        if resp.status_code == 200:
            data = resp.json()
            container_id = data.get('containerId', '')
            print(f"  Launched! Container: {container_id}")
            return str(container_id)
        else:
            print(f"  ERROR: {resp.status_code} - {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    stats = '--stats' in sys.argv
    export_nav = '--export-sales-nav' in sys.argv
    launch_nav = '--launch-sales-nav' in sys.argv

    if export_nav:
        export_sales_nav_contacts()
    elif launch_nav:
        # Usage: python phantombuster_etl.py --launch-sales-nav <google_sheet_url> [limit]
        remaining = [a for a in sys.argv[1:] if not a.startswith('--')]
        if not remaining:
            print("Usage: python phantombuster_etl.py --launch-sales-nav <sheet_url> [limit]")
            print("  sheet_url: Google Sheet URL with profileUrl column")
            print("  limit: Max leads per launch (default 25)")
            sys.exit(1)
        sheet_url = remaining[0]
        limit = int(remaining[1]) if len(remaining) > 1 else 25
        launch_lead_sender(sheet_url, limit=limit)
    else:
        run_etl(dry_run=dry, stats_only=stats)
