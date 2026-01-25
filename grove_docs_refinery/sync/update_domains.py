"""
Update Domain property for Grove Corpus documents.

Domain options: research, architecture, economics, strategy, protocol, spec
"""

from .api import get_api

GROVE_CORPUS_DB_ID = '00ea815de6fa40daa79bf5dd29b85a29'

# Manual domain assignments based on document titles and content
# Format: "title substring" -> "domain"
DOMAIN_ASSIGNMENTS = {
    # Research - technical analysis, papers, studies
    "Training Ratchet": "research",
    "Asymptotic Convergence": "research",
    "World Models and Memory": "research",
    "Local AI Infrastructure Capability": "research",
    "Chinese Open-Source AI": "research",
    "Chronicler as Cognitive Archaeology": "research",
    "Hivemind as Infrastructure": "research",
    "Research Intelligence Problem": "research",
    "Simulation Deep Dive": "research",

    # Architecture - system design, technical architecture
    "Kinetic Framework": "architecture",
    "Exploration Architecture Thesis": "architecture",
    "Sprout System": "architecture",
    "Exploration Architecture Summary": "architecture",
    "Trellis Architecture": "architecture",
    "Field Architecture": "architecture",
    "Bedrock Information Architecture": "architecture",
    "Kernel Codex": "architecture",
    "Grove Terminal: A Deep Dive": "architecture",

    # Strategy - business, go-to-market, positioning
    "Your Personal AI Village": "strategy",
    "Why Distributed AI Infrastructure": "strategy",
    "Purdue: Academic Strategy": "strategy",

    # Economics - tokenomics, incentives, value
    "Economics Deep Dive": "economics",

    # Protocol - processes, workflows, methodologies
    "Execution Protocol": "protocol",
    "Foundation Loop": "protocol",
    "A2UI Protocol": "protocol",

    # Spec - specifications, patterns, tools
    "Copilot Configurator": "spec",
    "User Story Refinery": "spec",
    "Pattern 10": "spec",
    "Refactoring Sprint": "spec",
    "Hygiene Launcher": "spec",
    "White Paper Prompt Kit": "spec",
}


def get_domain_for_title(title: str) -> str:
    """Match title to domain assignment."""
    for pattern, domain in DOMAIN_ASSIGNMENTS.items():
        if pattern.lower() in title.lower():
            return domain
    return ""


def update_domains(dry_run: bool = True):
    """Update Domain property for documents missing it."""
    api = get_api()

    print("Fetching Grove Corpus documents...")
    pages = api.query_database(GROVE_CORPUS_DB_ID)

    updates = []
    unmatched = []

    for page in pages:
        props = page.get('properties', {})

        # Get title
        title_prop = props.get('Title', {})
        title = ''.join(t.get('plain_text', '') for t in title_prop.get('title', []))

        # Check if domain is missing
        domain_prop = props.get('Domain', {})
        current_domain = domain_prop.get('select', {}).get('name', '') if domain_prop.get('select') else ''

        if current_domain:
            continue  # Already has domain

        # Find matching domain
        new_domain = get_domain_for_title(title)

        if new_domain:
            updates.append({
                'id': page['id'],
                'title': title,
                'domain': new_domain
            })
        else:
            unmatched.append(title)

    # Summary
    print(f"\nDocuments to update: {len(updates)}")
    print(f"Unmatched documents: {len(unmatched)}")

    if unmatched:
        print("\n--- Unmatched (need manual assignment) ---")
        for title in unmatched:
            print(f"  - {title}")

    print("\n--- Planned Updates ---")
    for update in updates:
        print(f"  [{update['domain']:<12}] {update['title'][:50]}")

    if dry_run:
        print("\n[DRY RUN] No changes made. Run with --apply to update Notion.")
        return updates

    # Apply updates
    print("\n--- Applying Updates ---")
    for update in updates:
        try:
            api.update_page(update['id'], {
                'Domain': {'select': {'name': update['domain']}}
            })
            print(f"  Updated: {update['title'][:40]}... -> {update['domain']}")
        except Exception as e:
            print(f"  ERROR: {update['title'][:40]}... - {e}")

    print(f"\nDone! Updated {len(updates)} documents.")
    return updates


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Update Domain property')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default: dry run)')
    args = parser.parse_args()

    update_domains(dry_run=not args.apply)


if __name__ == '__main__':
    main()
