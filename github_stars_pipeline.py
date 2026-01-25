"""
GitHub Starred Repos Pipeline
Fetches new stars daily, classifies them, adds to Notion with utility thoughts.
"""
import json
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
GITHUB_USERNAME = "twocash"
NOTION_DB_ID = "cbcb87b2-d89c-4af1-a883-0ce4245b3f53"
LAST_CHECKED_FILE = "last_checked_repos.json"

# Category keywords for classification
CATEGORY_KEYWORDS = {
    "AI Agents & Frameworks": ["agent", "mcp", "autonomous", "multi-agent", "metagpt", "adk", "agent-lightning"],
    "Claude Code/Skills": ["claude-code", "claude-skill", "claude", "skill", "subagent"],
    "Browser & Web Automation": ["browser", "automation", "scraper", "playwright", "puppeteer", "crawl"],
    "Memory & Knowledge": ["memory", "knowledge", "rag", "embeddings", "chroma", "supermemory", "openmemory"],
    "LLM/RAG/Vector DB": ["llm", "llama", "ollama", "vector", "faiss", "rag", "retrieval"],
    "Workflow & Automation": ["workflow", "n8n", "automation", "pipeline", "activepieces"],
    "Productivity Tools": ["productivity", "todo", "organize", "bookmark", "note", "manager"],
    "Design & UI": ["design", "ui", "figma", "component", "tailwind", "shadcn"],
    "Privacy & Local-First": ["privacy", "local", "self-hosted", "offline", "own-your-data"],
    "Image/Media/OCR": ["image", "ocr", "video", "upscaler", "generation", "flux", "pdf"],
    "Finance & Trading": ["trading", "finance", "stock", "crypto", "quant", "backtest", "vectorbt"]
}

# Utility thought templates
THOUGHT_TEMPLATES = {
    "AI Agents & Frameworks": "Could integrate into multi-agent orchestration for complex workflows. Consider using for: {}",
    "Claude Code/Skills": "Potential skill or subagent for Claude Code. Would enhance: {}",
    "Browser & Web Automation": "Useful for end-to-end testing or data extraction pipelines. Apply to: {}",
    "Memory & Knowledge": "Could enhance long-term context for AI agents. Great for: {}",
    "LLM/RAG/Vector DB": "Essential infrastructure for RAG pipelines. Use case: {}",
    "Workflow & Automation": "Automates repetitive tasks. Streamlines: {}",
    "Productivity Tools": "Daily driver potential. Improves: {}",
    "Design & UI": "Frontend development acceleration. Speed up: {}",
    "Privacy & Local-First": "Data sovereignty focus. Keep for: {}",
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
    return "Productivity Tools"  # Default category

def generate_thought(repo: Dict, category: str) -> str:
    """Generate a utility thought for the repo."""
    # Extract key terms from repo
    key_terms = []
    if repo["topics"]:
        key_terms = repo["topics"][:3]
    else:
        # Extract from description
        words = repo["description"].split()[:5]
        key_terms = [w for w in words if len(w) > 3]

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

def main():
    """Main pipeline."""
    print(f"[{datetime.now().isoformat()}] Starting GitHub stars pipeline...")

    # Load known repos
    known_repos = load_last_checked()
    print(f"Loaded {len(known_repos)} known repos")

    # Fetch new stars
    new_repos = fetch_starred_repos()
    print(f"Found {len(new_repos)} starred repos")

    # Filter to only new ones
    new_only = [r for r in new_repos if r["url"] not in known_repos]
    print(f"New repos: {len(new_only)}")

    if not new_only:
        print("No new repos to process.")
        return

    # Process and add to Notion
    all_urls = set(known_repos)

    for repo in new_only:
        category = classify_repo(repo)
        thought = generate_thought(repo, category)

        print(f"  - {repo['name']} -> {category}")

        # Add to Notion (via MCP - see below for implementation)
        add_to_notion(repo, category, thought)

        all_urls.add(repo["url"])

    # Save updated list
    save_last_checked(all_urls)
    print(f"Updated last_checked with {len(all_urls)} total repos")
    print("Pipeline complete!")

def add_to_notion(repo: Dict, category: str, thought: str):
    """
    Add repo to Notion database.
    Note: This requires the Notion MCP server or direct API access.
    For CLI version, use: python -c "
    from notion_client import Client
    client = Client(auth=NOTION_API_KEY)
    client.pages.create(parent={'database_id': NOTION_DB_ID}, properties={...})
    "
    """
    # Placeholder - actual implementation depends on Notion API setup
    # See: https://github.com/ramnes/notion-client or official SDK
    pass

if __name__ == "__main__":
    main()
