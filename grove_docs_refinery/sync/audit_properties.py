"""
Audit Grove Corpus documents for missing properties.
"""

from .api import get_api

GROVE_CORPUS_DB_ID = '00ea815de6fa40daa79bf5dd29b85a29'


def extract_property(props: dict, name: str, prop_type: str = 'select') -> str:
    """Extract a property value from Notion properties."""
    prop = props.get(name, {})

    if prop_type == 'title':
        return ''.join(t.get('plain_text', '') for t in prop.get('title', []))
    elif prop_type == 'select':
        select = prop.get('select')
        return select.get('name', '') if select else ''
    elif prop_type == 'date':
        date = prop.get('date')
        return date.get('start', '') if date else ''
    elif prop_type == 'rich_text':
        return ''.join(t.get('plain_text', '') for t in prop.get('rich_text', []))

    return ''


def audit_properties():
    """Audit all documents for missing properties."""
    api = get_api()

    print("Fetching Grove Corpus documents...")
    pages = api.query_database(GROVE_CORPUS_DB_ID)
    print(f"Found {len(pages)} documents\n")

    # Track missing properties
    missing_date = []
    missing_domain = []
    missing_author = []

    print("=" * 80)
    print(f"{'Title':<50} {'Date':<12} {'Domain':<12} {'Author':<10}")
    print("=" * 80)

    for page in pages:
        props = page.get('properties', {})

        title = extract_property(props, 'Title', 'title')[:48]
        date = extract_property(props, 'Date', 'date')
        domain = extract_property(props, 'Domain', 'select')
        author = extract_property(props, 'Author', 'rich_text')
        doc_type = extract_property(props, 'Type', 'select')

        # Track missing
        page_info = {
            'id': page['id'],
            'title': title,
            'type': doc_type
        }

        if not date:
            missing_date.append(page_info)
            date = '(missing)'
        if not domain:
            missing_domain.append(page_info)
            domain = '(missing)'
        if not author:
            missing_author.append(page_info)
            author = '(missing)'

        print(f"{title:<50} {date:<12} {domain:<12} {author:<10}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total documents: {len(pages)}")
    print(f"Missing Date:    {len(missing_date)}")
    print(f"Missing Domain:  {len(missing_domain)}")
    print(f"Missing Author:  {len(missing_author)}")

    if missing_domain:
        print("\n--- Documents Missing Domain ---")
        for doc in missing_domain:
            print(f"  [{doc['type']}] {doc['title']}")

    return {
        'total': len(pages),
        'missing_date': missing_date,
        'missing_domain': missing_domain,
        'missing_author': missing_author
    }


if __name__ == '__main__':
    audit_properties()
