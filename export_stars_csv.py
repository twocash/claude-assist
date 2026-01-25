#!/usr/bin/env python3
"""
Export GitHub starred repos to CSV for Notion import.
"""
import json
import csv

with open('starred_repos.json', 'r', encoding='utf-8') as f:
    repos = json.load(f)

CATEGORY_KEYWORDS = {
    'AI Agents & Frameworks': ['agent', 'mcp', 'autonomous', 'multi-agent', 'metagpt', 'adk', 'agent-lightning', 'mastra', 'letta', 'dexter'],
    'Claude Code/Skills': ['claude-code', 'claude-skill', 'claude', 'skill', 'subagent', 'claude-code-skills', 'claude-code-plugin'],
    'Browser & Web Automation': ['browser', 'automation', 'scraper', 'playwright', 'puppeteer', 'crawl', 'web-automation', 'chrome-devtools'],
    'Memory & Knowledge': ['memory', 'knowledge', 'rag', 'embeddings', 'chroma', 'supermemory', 'openmemory', 'claude-mem', 'davia'],
    'LLM/RAG/Vector DB': ['llm', 'llama', 'ollama', 'vector', 'faiss', 'rag', 'retrieval', 'vectorbt', 'llmrouter', 'leann'],
    'Workflow & Automation': ['workflow', 'n8n', 'automation', 'pipeline', 'activepieces', 'agor'],
    'Productivity Tools': ['productivity', 'todo', 'organize', 'bookmark', 'note', 'manager', 'gerbil', 'dayflow'],
    'Design & UI': ['design', 'ui', 'figma', 'component', 'tailwind', 'shadcn', 'onlook', 'webstudio', 'dembrandt'],
    'Privacy & Local-First': ['privacy', 'local', 'self-hosted', 'offline', 'own-your-data', 'linkwarden', 'bentopdf'],
    'Image/Media/OCR': ['image', 'ocr', 'video', 'upscaler', 'generation', 'flux', 'pdf', 'upscayl', 'pdfcraft', 'chandra'],
    'Finance & Trading': ['trading', 'finance', 'stock', 'crypto', 'quant', 'backtest', 'vectorbt', 'dexter']
}

THOUGHT_TEMPLATES = {
    'AI Agents & Frameworks': 'Foundational tool for multi-agent orchestration. Could integrate into: {}',
    'Claude Code/Skills': 'Potential Claude Code skill. Would enhance: {}',
    'Browser & Web Automation': 'Essential for browser-based automation. Apply to: {}',
    'Memory & Knowledge': 'Enhances long-term context for AI agents. Great for: {}',
    'LLM/RAG/Vector DB': 'Essential RAG infrastructure. Use case: {}',
    'Workflow & Automation': 'Streamlines repetitive tasks. Automates: {}',
    'Productivity Tools': 'Daily driver potential. Improves: {}',
    'Design & UI': 'Frontend acceleration. Speed up: {}',
    'Privacy & Local-First': 'Data sovereignty focused. Keep for: {}',
    'Image/Media/OCR': 'Media processing pipeline. Useful for: {}',
    'Finance & Trading': 'Quantitative analysis. Apply to: {}'
}

def classify_repo(repo):
    text = f"{repo['name']} {repo['description']} {','.join(repo['topics'])}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    return 'Productivity Tools'

def generate_thought(repo, category):
    key_terms = repo['topics'][:3] if repo['topics'] else []
    if not key_terms:
        words = [w for w in repo['description'].split() if len(w) > 3][:5]
        key_terms = words
    template = THOUGHT_TEMPLATES.get(category, 'Could be useful for: {}')
    return template.format(', '.join(key_terms) if key_terms else 'general development')

# Write CSV
with open('github_stars_export.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(['Name', 'Category', 'Language', 'Stars', 'URL', 'Description', 'Thought', 'Topics'])
    for r in repos:
        cat = classify_repo(r)
        thought = generate_thought(r, cat)
        topics = ','.join(r['topics'])
        writer.writerow([r['name'], cat, r['language'], r['stars'], r['url'], r['description'], thought, topics])

print(f"Exported {len(repos)} repos to github_stars_export.csv")
