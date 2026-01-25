#!/usr/bin/env python3
"""
Standardize GitHub starred repo titles with pattern:
{CATEGORY} | {CLASS} | {FEATURE} | {BENEFIT}

And generate structured tags for Notion database.
"""
import json

with open('starred_repos.json', 'r', encoding='utf-8') as f:
    repos = json.load(f)

# Category short codes
CAT_CODES = {
    'AI Agents & Frameworks': 'AGENT',
    'Claude Code/Skills': 'CLAUDE',
    'Browser & Web Automation': 'BROWSER',
    'Memory & Knowledge': 'MEMORY',
    'LLM/RAG/Vector DB': 'LLM',
    'Workflow & Automation': 'WORKFLOW',
    'Productivity Tools': 'TOOL',
    'Design & UI': 'UI',
    'Privacy & Local-First': 'LOCAL',
    'Image/Media/OCR': 'MEDIA',
    'Finance & Trading': 'FINANCE'
}

# Class mappings
CLASSES = {
    'agent': ['agent', 'autonomous', 'agentic'],
    'framework': ['framework', 'platform', 'system', 'library'],
    'multi-agent': ['multi-agent', 'multi agent', 'collaborative', 'crew', 'society'],
    'skill': ['skill', 'plugin', 'extension', 'add-on'],
    'setup': ['setup', 'config', 'template', 'starter', 'boilerplate'],
    'workflow': ['workflow', 'pattern', 'practice', 'methodology'],
    'browser': ['browser', 'headless', 'chrome', 'chromium'],
    'scraper': ['scrap', 'extract', 'crawl', 'spider'],
    'automation': ['automation', 'auto', 'robotic', 'rpa'],
    'memory': ['memory', 'persistent', 'store', 'remember'],
    'knowledge': ['knowledge', 'base', 'wiki', 'doc'],
    'rag': ['rag', 'retrieval', 'embeddings', 'vector search'],
    'chunking': ['chunk', 'split', 'segment', 'partition'],
    'vector-db': ['vector', 'database', 'faiss', 'chroma', 'pinecone'],
    'router': ['router', 'route', 'dispatch', 'select'],
    'workflow-tool': ['workflow', 'pipeline', 'n8n', 'activepieces'],
    'app': ['app', 'application', 'desktop'],
    'tool': ['tool', 'utility', 'manager', 'helper'],
    'bookmark': ['bookmark', 'save', 'collect', 'link'],
    'builder': ['builder', 'generator', 'create', 'scaffold'],
    'component': ['component', 'ui', 'widget', 'library'],
    'design-system': ['design-system', 'tokens', 'figma', 'style'],
    'local': ['local', 'offline', 'desktop', 'electron'],
    'self-hosted': ['self-hosted', 'selfhosted', 'docker'],
    'ocr': ['ocr', 'recognition', 'text extraction'],
    'pdf': ['pdf', 'document', 'viewer', 'editor'],
    'upscaling': ['upscale', 'super-resolution', 'enhance'],
    'image-gen': ['image', 'generation', 'flux', 'sdxl'],
    'trading': ['trading', 'trade', 'exchange'],
    'backtest': ['backtest', 'back-testing', 'simulation'],
    'quant': ['quant', 'quantitative', 'algorithm', 'strategy'],
}

# Feature keywords
FEATURES = {
    'multi-model': ['multi-model', 'multi model', 'any model', 'any llm'],
    'visual': ['visual', 'design', 'ui', 'interface'],
    'local-first': ['local', 'offline', 'private', 'your data'],
    'browser-native': ['browser', 'in-browser', 'web-based'],
    'free': ['free', 'open-source', 'opensource', 'gratis'],
    'autonomous': ['autonomous', 'automatic', 'auto', 'self-running'],
    'persistent': ['persistent', 'continuous', 'never stop'],
    'multiplayer': ['multiplayer', 'collaborative', 'team', 'shared'],
    'memory': ['memory', 'remember', 'context', 'long-term'],
    'fast': ['fast', 'quick', 'speedy', 'lightning', 'performance'],
    'claude-native': ['claude', 'claude code', 'anthropic'],
    'self-hosted': ['self-hosted', 'selfhosted', 'your server'],
    'ai-powered': ['ai', 'llm', 'gpt', 'agent'],
    'agentic': ['agent', 'agentic', 'autonomous'],
}

# Benefit keywords
BENEFITS = {
    'industry-standard': ['25k', '50k', '60k', 'widely used', 'industry'],
    'widely-trusted': ['5k', '10k', '20k', 'popular', 'trusted'],
    'proven': ['1k', '2k', '3k', 'proven', 'reliable'],
    'data-sovereignty': ['privacy', 'private', 'local', 'your data', 'control'],
    'zero-cost': ['free', 'open-source', 'no cost', 'gratis'],
    'hands-free': ['autonomous', 'automatic', 'auto', 'self-running'],
    'never-lose-context': ['memory', 'persistent', 'remember', 'context'],
    'ai-native': ['ai', 'llm', 'agent', 'claude', 'gpt'],
    'boost-productivity': ['productivity', 'efficient', 'save time', 'faster'],
    'full-control': ['self-hosted', 'local', 'own your data'],
}

def classify_repo(repo: Dict) -> str:
    """Classify repo into category."""
    text = f"{repo['name']} {repo['description']} {' '.join(repo['topics'])}".lower()

    keywords_cat = [
        (['claude', 'skill', 'plugin'], 'Claude Code/Skills'),
        (['browser', 'automation', 'scraper', 'crawl', 'chrome-devtools'], 'Browser & Web Automation'),
        (['memory', 'rag', 'knowledge', 'embeddings', 'chroma', 'claude-mem'], 'Memory & Knowledge'),
        (['vector', 'llm', 'chunk', 'router', 'ollama', 'llama'], 'LLM/RAG/Vector DB'),
        (['workflow', 'n8n', 'pipeline'], 'Workflow & Automation'),
        (['design', 'ui', 'figma', 'component', 'builder'], 'Design & UI'),
        (['privacy', 'local', 'self-hosted', 'offline', 'own-your-data'], 'Privacy & Local-First'),
        (['pdf', 'ocr', 'image', 'upscaling', 'flux'], 'Image/Media/OCR'),
        (['trading', 'finance', 'quant', 'backtest', 'vectorbt'], 'Finance & Trading'),
        (['agent', 'mcp', 'multi-agent', 'framework'], 'AI Agents & Frameworks'),
    ]

    for keywords, category in keywords_cat:
        if any(k in text for k in keywords):
            return category
    return 'Productivity Tools'

def extract_class(repo: Dict) -> str:
    """Extract class/type from repo."""
    text = f"{repo['description']} {' '.join(repo['topics'])}".lower()

    for cls, keywords in CLASSES.items():
        if any(k in text for k in keywords):
            return cls.replace('-', ' ').title()
    return 'Tool'

def extract_feature(repo: Dict) -> str:
    """Extract key feature."""
    text = f"{repo['description']} {' '.join(repo['topics'])}".lower()

    for feature, keywords in FEATURES.items():
        if any(k in text for k in keywords):
            return feature.replace('-', ' ').title()

    # Fallback to first meaningful words
    words = repo.get('description', '').split()[:4]
    meaningful = [w for w in words if len(w) > 4 and w.isalnum()]
    return ' '.join(meaningful).title() if meaningful else 'Utility'

def extract_benefit(repo: Dict) -> str:
    """Extract key benefit."""
    text = f"{repo['description']} {' '.join(repo['topics'])}".lower()
    stars = repo.get('stars', 0)

    if stars > 20000:
        return 'Industry Standard'
    elif stars > 5000:
        return 'Widely Trusted'
    elif stars > 1000:
        return 'Proven & Popular'

    for benefit, keywords in BENEFITS.items():
        if any(k in text for k in keywords):
            return benefit.replace('-', ' ').title()

    return 'Boost Productivity'

def generate_tags(repo: Dict) -> dict:
    """Generate structured tags."""
    text = f"{repo['description']} {repo['name']} {' '.join(repo['topics'])}".lower()

    tags = {
        'platform': 'cloud',  # default
        'cost': 'oss',  # default
        'type': 'api',  # default
        'maturity': 'production',
    }

    # Platform
    if any(w in text for w in ['local', 'offline', 'desktop', 'electron', 'self-hosted', 'selfhosted']):
        tags['platform'] = 'local'
    elif any(w in text for w in ['browser', 'extension', 'in-browser']):
        tags['platform'] = 'browser'

    # Cost
    if 'paid' in text or 'pro' in text or 'premium' in text:
        tags['cost'] = 'paid'
    elif any(w in text for w in ['free', 'open-source', 'opensource', 'gratis']):
        tags['cost'] = 'free'

    # Type
    if any(w in text for w in ['cli', 'command', 'terminal']):
        tags['type'] = 'cli'
    elif any(w in text for w in ['app', 'desktop', 'electron', 'gui']):
        tags['type'] = 'gui'
    elif any(w in text for w in ['browser', 'extension']):
        tags['type'] = 'browser-ext'

    # Maturity
    if any(w in text for w in ['experimental', 'alpha', 'beta', 'new']):
        tags['maturity'] = 'experimental'
    elif any(w in text for w in ['stable', 'production', 'reliable']):
        tags['maturity'] = 'production'

    return tags

# Process all repos
entries = []
for r in repos:
    category = classify_repo(r)
    cat_code = CAT_CODES.get(category, 'TOOL')
    klass = extract_class(r)
    feature = extract_feature(r)
    benefit = extract_benefit(r)
    tags = generate_tags(r)

    # Format: AGENT | Framework | Multi-Model | Industry Standard
    title = f"{cat_code} | {klass} | {feature} | {benefit}"

    entries.append({
        'title': title,
        'category': category,
        'class': klass,
        'feature': feature,
        'benefit': benefit,
        'platform': tags['platform'],
        'cost': tags['cost'],
        'type': tags['type'],
        'maturity': tags['maturity'],
        'url': r['url'],
        'stars': r['stars'],
        'original_name': r['name'],
        'description': r['description'][:200],
    })

# Print summary
print("TITLE PATTERN: {CAT} | {CLASS} | {FEATURE} | {BENEFIT}")
print("=" * 65)
print("\nSAMPLE ENTRIES:\n")

for e in entries[:12]:
    print(f"Title: {e['title']}")
    print(f"  Tags: platform={e['platform']} | cost={e['cost']} | type={e['type']} | maturity={e['maturity']}")
    print(f"  Original: {e['original_name']}")
    print()

print("=" * 65)
print(f"TOTAL: {len(entries)} entries")

# Tag distribution
print("\nTAG DISTRIBUTION:")
for tag_type in ['platform', 'cost', 'type', 'maturity']:
    counts = {}
    for e in entries:
        counts[e[tag_type]] = counts.get(e[tag_type], 0) + 1
    print(f"\n  {tag_type.upper()}:")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v}")

# Save for Notion
output = {
    'entries': entries,
    'count': len(entries),
    'title_pattern': '{CAT} | {CLASS} | {FEATURE} | {BENEFIT}',
    'tag_schema': {
        'platform': ['local', 'cloud', 'browser', 'cli', 'gui', 'browser-ext', 'api'],
        'cost': ['free', 'paid', 'freemium', 'oss'],
        'type': ['api', 'cli', 'gui', 'browser-ext', 'library'],
        'maturity': ['experimental', 'beta', 'production']
    }
}

with open('standardized_repos.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nSaved to standardized_repos.json")
