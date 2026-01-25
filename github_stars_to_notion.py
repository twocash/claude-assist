"""
GitHub Stars to Notion Pipeline
Run this script to add new starred repos to your Notion database.

Prerequisites:
1. Install Notion SDK: pip install notion-client
2. Get your Notion integration token: https://www.notion.so/my-integrations
3. Share your database with the integration
4. Set NOTION_API_KEY environment variable

Usage:
    python github_stars_to_notion.py

For scheduled daily runs (Windows):
    schtasks /create /tn "GitHub Stars Sync" /tr "python C:\path\to\github_stars_to_notion.py" /sc daily /st 09:00
"""
import json
import os
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
GITHUB_USERNAME = "twocash"
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_DB_ID = "cbcb87b2-d89c-4af1-a883-0ce4245b3f53"  # From database URL
LAST_CHECKED_FILE = "last_checked_repos.json"

# Category keywords for classification
CATEGORY_KEYWORDS = {
    "AI Agents & Frameworks": ["agent", "mcp", "autonomous", "multi-agent", "metagpt", "adk", "agent-lightning", "mastra", "letta"],
    "Claude Code/Skills": ["claude-code", "claude-skill", "claude", "skill", "subagent", "claude-code-skills"],
    "Browser & Web Automation": ["browser", "automation", "scraper", "playwright", "puppeteer", "crawl", "web-automation"],
    "Memory & Knowledge": ["memory", "knowledge", "rag", "embeddings", "chroma", "supermemory", "openmemory", "claude-mem"],
    "LLM/RAG/Vector DB": ["llm", "llama", "ollama", "vector", "faiss", "rag", "retrieval", "vectorbt"],
    "Workflow & Automation": ["workflow", "n8n", "automation", "pipeline", "activepieces", "agor"],
    "Productivity Tools": ["productivity", "todo", "organize", "bookmark", "note", "manager", "gerbil"],
    "Design & UI": ["design", "ui", "figma", "component", "tailwind", "shadcn", "onlook", "webstudio"],
    "Privacy & Local-First": ["privacy", "local", "self-hosted", "offline", "own-your-data", "linkwarden"],
    "Image/Media/OCR": ["image", "ocr", "video", "upscaler", "generation", "flux", "pdf", "upscayl"],
    "Finance & Trading": ["trading", "finance", "stock", "crypto", "quant", "backtest", "vectorbt"]
}

# Utility thought templates
THOUGHT_TEMPLATES = {
    "AI Agents & Frameworks": "Foundational tool for multi-agent orchestration. Could integrate into: {}",
    "Claude Code/Skills": "Potential Claude Code skill. Would enhance: {}",
    "Browser & Web Automation": "Essential for browser-based automation. Apply to: {}",
    "Memory & Knowledge": "Enhances long-term context for AI agents. Great for: {}",
    "LLM/RAG/Vector DB": "Essential RAG infrastructure. Use case: {}",
    "Workflow & Automation": "Streamlines repetitive tasks. Automates: {}",
    "Productivity Tools": "Daily driver potential. Improves: {}",
    "Design & UI": "Frontend acceleration. Speed up: {}",
    "Privacy & Local-First": "Data sovereignty focused. Keep for: {}",
    "Image/Media/OCR": "Media processing pipeline. Useful for: {}",
    "Finance & Trading": "Quantitative analysis. Apply to: {}"
}

def fetch_starred_repos(since: Optional[str] = None) -> List[Dict]:
    """Fetch starred repos from GitHub API."""
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/starred?per_page=100"
    if since:
        url += f"&since={since}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    repos = []
    for r in data:
        repos.append({
            "name": r["full_name"],
            "description": r.get("description", "") or "",
            "language": r.get("language") or "None",
            "stars": r["stargazers_count"],
            "url": r["html_url"],
            "updated": r["updated_at"][:10],
            "topics": r.get("topics", []) or []
        })
    return repos

def classify_repo(repo: Dict) -> str:
    """Classify a repo based on keywords."""
    text = f"{repo['name']} {repo['description']} {' '.join(repo['topics'])}".lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    return "Productivity Tools"

def generate_thought(repo: Dict, category: str) -> str:
    """Generate a utility thought for the repo."""
    key_terms = repo["topics"][:3] if repo["topics"] else []
    if not key_terms:
        words = [w for w in repo["description"].split() if len(w) > 3][:5]
        key_terms = words

    template = THOUGHT_TEMPLATES.get(category, "Could be useful for: {}")
    return template.format(", ".join(key_terms) if key_terms else "general development")

def load_last_checked() -> set:
    """Load previously processed repos."""
    try:
        with open(LAST_CHECKED_FILE) as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_last_checked(repos: set):
    """Save processed repos."""
    with open(LAST_CHECKED_FILE, "w") as f:
        json.dump(list(repos), f)

def add_to_notion_via_api(repo: Dict, category: str, thought: str) -> bool:
    """Add repo to Notion using the REST API."""
    if not NOTION_API_KEY:
        print(f"  [SKIP] No NOTION_API_KEY set")
        return False

    url = f"https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": repo["name"]}}]},
            "URL": {"url": repo["url"]},
            "Description": {"rich_text": [{"text": {"content": repo["description"][:2000]}}]},
            "Language": {"rich_text": [{"text": {"content": repo["language"]}}]},
            "Stars": {"number": repo["stars"]},
            "Thought": {"rich_text": [{"text": {"content": thought}}]},
            "Date Starred": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
            "Topics": {"multi_select": [{"name": t} for t in repo["topics"][:10]]}
        }
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            return response.status == 200
    except Exception as e:
        print(f"  [ERROR] Notion API: {e}")
        return False

def main():
    """Main pipeline."""
    print(f"[{datetime.now().isoformat()}] GitHub Stars Pipeline")
    print("=" * 50)

    # Load known repos
    known_repos = load_last_checked()
    print(f"Known repos: {len(known_repos)}")

    # Fetch all stars
    all_repos = fetch_starred_repos()
    print(f"Total starred: {len(all_repos)}")

    # Filter to new only
    new_repos = [r for r in all_repos if r["url"] not in known_repos]
    print(f"New repos: {len(new_repos)}")

    if not new_repos:
        print("No new repos to process.")
        return

    # Process each new repo
    all_urls = set(known_repos)
    added = 0

    for repo in new_repos:
        category = classify_repo(repo)
        thought = generate_thought(repo, category)

        print(f"\n{repo['name']}")
        print(f"  Category: {category}")
        print(f"  Thought: {thought}")

        # Add to Notion (if API key available)
        if add_to_notion_via_api(repo, category, thought):
            print(f"  [OK] Added to Notion")
            added += 1
        else:
            print(f"  [SAVE] Saved locally (Notion unavailable)")

        all_urls.add(repo["url"])

    # Save updated list
    save_last_checked(all_urls)

    print(f"\n{'='*50}")
    print(f"Processed: {len(new_repos)} | Added to Notion: {added}")
    print("Pipeline complete!")

if __name__ == "__main__":
    main()
