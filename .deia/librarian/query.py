#!/usr/bin/env python3
"""
DEIA Librarian - MVP Query Tool
Simple keyword-based search of Global Commons index

Usage:
    python query.py "DNS not working"
    python query.py "deployment failed"
    python query.py --platform netlify
"""

import yaml
import sys
import os
from pathlib import Path

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Path to index file
INDEX_PATH = Path(__file__).parent.parent / "index" / "master-index.yaml"

def load_index():
    """Load the YAML index file"""
    if not INDEX_PATH.exists():
        print(f"Error: Index file not found at {INDEX_PATH}")
        sys.exit(1)

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def extract_keywords(query):
    """Extract keywords from query string"""
    # Simple tokenization (lowercase, split on spaces/punctuation)
    import re
    tokens = re.findall(r'\w+', query.lower())
    return set(tokens)

def search_index(index, query_keywords):
    """Search index for matching documents"""
    results = []

    # Search through clusters
    for cluster_name, cluster_data in index.get('clusters', {}).items():
        if not isinstance(cluster_data, dict):
            continue

        # Check cluster keywords
        cluster_keywords = set(k.lower() for k in cluster_data.get('keywords', []))
        cluster_match = bool(query_keywords & cluster_keywords)

        # Search documents in cluster
        documents = cluster_data.get('documents', [])
        if not isinstance(documents, list):
            continue

        for doc in documents:
            if not isinstance(doc, dict):
                continue

            # Skip cross-reference IDs (strings without full metadata)
            if not doc.get('path'):
                continue

            # Check doc keywords
            doc_keywords = set(k.lower() for k in doc.get('keywords', []))
            doc_match = bool(query_keywords & doc_keywords)

            # Calculate match score
            score = 0
            if cluster_match:
                score += 1
            if doc_match:
                score += 2

            # Check title/summary for keywords
            title_words = set(doc.get('title', '').lower().split())
            summary_words = set(doc.get('summary', '').lower().split())
            if query_keywords & title_words:
                score += 3
            if query_keywords & summary_words:
                score += 1

            if score > 0:
                results.append({
                    'doc': doc,
                    'cluster': cluster_name,
                    'score': score,
                    'matched_keywords': query_keywords & (cluster_keywords | doc_keywords)
                })

    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def format_result(result, index=None):
    """Format a single result for display"""
    doc = result['doc']
    cluster = result['cluster']
    score = result['score']

    # Urgency indicator
    urgency = doc.get('urgency', 'unknown')
    if urgency == 'critical':
        urgency_icon = '⚡'
    elif urgency == 'high':
        urgency_icon = '⚠️'
    elif urgency == 'medium':
        urgency_icon = '📝'
    else:
        urgency_icon = '📚'

    # Format output
    output = []
    output.append(f"\n{urgency_icon} {doc['title']}")
    output.append(f"   {doc['summary']}")
    output.append(f"   📁 {doc['path']}")
    output.append(f"   🏷️  Cluster: {cluster} | Urgency: {urgency.upper()}")

    # Show matched keywords
    if result.get('matched_keywords'):
        keywords_str = ', '.join(sorted(result['matched_keywords']))
        output.append(f"   🔍 Matched: {keywords_str}")

    return '\n'.join(output)

def platform_filter(index, platform):
    """Get all docs for a specific platform"""
    platform_idx = index.get('platform_index', {})
    doc_ids = platform_idx.get(platform.lower(), [])

    results = []
    for cluster_name, cluster_data in index.get('clusters', {}).items():
        if not isinstance(cluster_data, dict):
            continue
        for doc in cluster_data.get('documents', []):
            if not isinstance(doc, dict) or not doc.get('path'):
                continue
            if doc.get('id') in doc_ids:
                results.append({
                    'doc': doc,
                    'cluster': cluster_name,
                    'score': 5,  # High score for exact platform match
                    'matched_keywords': {platform.lower()}
                })

    return results

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python query.py <query>")
        print("       python query.py --platform <platform>")
        print("\nExamples:")
        print("  python query.py \"DNS not working\"")
        print("  python query.py \"deployment failed\"")
        print("  python query.py --platform netlify")
        sys.exit(1)

    # Load index
    print("Loading index...")
    index = load_index()
    print(f"Loaded {index.get('total_documents', 0)} documents in {index.get('total_clusters', 0)} clusters\n")

    # Parse arguments
    if sys.argv[1] == '--platform':
        if len(sys.argv) < 3:
            print("Error: --platform requires a platform name")
            sys.exit(1)
        platform = sys.argv[2]
        print(f"Searching for platform: {platform}\n")
        print("=" * 70)
        results = platform_filter(index, platform)
    else:
        query = ' '.join(sys.argv[1:])
        print(f"Query: \"{query}\"\n")
        print("=" * 70)

        # Extract keywords and search
        keywords = extract_keywords(query)
        print(f"Keywords: {', '.join(sorted(keywords))}\n")
        results = search_index(index, keywords)

    # Display results
    if not results:
        print("\n❌ No matching documents found.")
        print("\nTry:")
        print("  - Broader keywords (e.g., 'deployment' instead of 'failed deployment')")
        print("  - Platform filter: --platform netlify")
        print("  - Check QUICK-REFERENCE.md for all available docs")
    else:
        print(f"\n✅ Found {len(results)} matching document(s):\n")
        for i, result in enumerate(results[:5], 1):  # Show top 5
            print(format_result(result, index))

        if len(results) > 5:
            print(f"\n... and {len(results) - 5} more. Refine query for better results.")

    print("\n" + "=" * 70)
    print(f"\n💡 Index version: {index.get('version', 'unknown')}")
    print(f"   Last updated: {index.get('last_updated', 'unknown')}")

if __name__ == '__main__':
    main()
