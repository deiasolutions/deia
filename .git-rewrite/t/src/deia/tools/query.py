#!/usr/bin/env python3
"""
DEIA Librarian - Enhanced Query Tool
Advanced search of Global Commons index with fuzzy matching, filters, and usage tracking

Usage:
    python query.py "DNS not working"
    python query.py "deployment failed" --urgency critical
    python query.py "python encoding" --platform windows
    python query.py "coordination" AND "governance"
    python query.py "deployment" OR "release" --audience advanced
"""

import yaml
import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional

try:
    from rapidfuzz import fuzz
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False
    print("Warning: rapidfuzz not installed. Fuzzy matching disabled.", file=sys.stderr)

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent.parent
INDEX_PATH = REPO_ROOT / ".deia" / "index" / "master-index.yaml"
LOGS_DIR = REPO_ROOT / ".deia" / "logs"
USAGE_LOG_PATH = LOGS_DIR / "librarian-queries.jsonl"

# Configuration
FUZZY_THRESHOLD = 80  # Minimum similarity score for fuzzy match (0-100)
DEFAULT_LIMIT = 5     # Number of results to show


def ensure_logs_dir():
    """Create logs directory if it doesn't exist"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log_query(query: str, filters: Dict, results_count: int, logic_mode: str = "AND"):
    """Log query to usage tracking file"""
    try:
        ensure_logs_dir()
        log_entry = {
            "ts": datetime.now().astimezone().isoformat(),
            "query": query,
            "logic": logic_mode,
            "filters": filters,
            "results": results_count,
            "fuzzy_enabled": FUZZY_AVAILABLE
        }

        with open(USAGE_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"Warning: Failed to log query: {e}", file=sys.stderr)


def load_index() -> Dict:
    """Load the YAML index file"""
    if not INDEX_PATH.exists():
        print(f"Error: Index file not found at {INDEX_PATH}")
        sys.exit(1)

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def extract_keywords(query: str) -> Set[str]:
    """Extract keywords from query string"""
    import re
    tokens = re.findall(r'\w+', query.lower())
    return set(tokens)


def fuzzy_match(text: str, query_keywords: Set[str], threshold: int = FUZZY_THRESHOLD) -> tuple[bool, int]:
    """
    Perform fuzzy matching on text against query keywords
    Returns: (matched: bool, best_score: int)
    """
    if not FUZZY_AVAILABLE:
        return False, 0

    text_lower = text.lower()
    best_score = 0

    for keyword in query_keywords:
        # Try partial ratio for substring matching
        score = fuzz.partial_ratio(keyword, text_lower)
        if score > best_score:
            best_score = score

    return best_score >= threshold, best_score


def search_index(
    index: Dict,
    query_keywords: Set[str],
    logic_mode: str = "AND",
    urgency_filter: Optional[str] = None,
    platform_filter: Optional[str] = None,
    audience_filter: Optional[str] = None,
    use_fuzzy: bool = True
) -> List[Dict]:
    """
    Search index for matching documents with advanced filtering

    Args:
        index: Loaded index data
        query_keywords: Set of keywords to search for
        logic_mode: "AND" (all keywords) or "OR" (any keyword)
        urgency_filter: Filter by urgency level (critical, high, medium, low)
        platform_filter: Filter by platform
        audience_filter: Filter by audience
        use_fuzzy: Enable fuzzy matching for typo tolerance
    """
    results = []

    # Search through clusters
    for cluster_name, cluster_data in index.get('clusters', {}).items():
        if not isinstance(cluster_data, dict):
            continue

        # Check cluster keywords
        cluster_keywords = set(k.lower() for k in cluster_data.get('keywords', []))

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

            # Apply filters first
            if urgency_filter and doc.get('urgency', '').lower() != urgency_filter.lower():
                continue

            if platform_filter:
                doc_platforms = [p.lower() for p in doc.get('platforms', [])]
                if platform_filter.lower() not in doc_platforms:
                    continue

            if audience_filter and doc.get('audience', '').lower() != audience_filter.lower():
                continue

            # Check doc keywords
            doc_keywords = set(k.lower() for k in doc.get('keywords', []))

            # Combine all searchable text
            title_words = set(doc.get('title', '').lower().split())
            summary_words = set(doc.get('summary', '').lower().split())
            all_doc_keywords = cluster_keywords | doc_keywords | title_words | summary_words

            # Calculate match score
            score = 0
            matched_keywords = set()
            fuzzy_matches = []

            # Exact keyword matching
            exact_matches = query_keywords & all_doc_keywords

            if logic_mode == "AND":
                # AND mode: all keywords must match (exact or fuzzy)
                keywords_matched = 0

                for kw in query_keywords:
                    if kw in all_doc_keywords:
                        keywords_matched += 1
                        matched_keywords.add(kw)
                        score += 2
                    elif use_fuzzy and FUZZY_AVAILABLE:
                        # Try fuzzy matching on title and summary
                        title_match, title_score = fuzzy_match(doc.get('title', ''), {kw})
                        summary_match, summary_score = fuzzy_match(doc.get('summary', ''), {kw})

                        if title_match:
                            keywords_matched += 1
                            matched_keywords.add(kw)
                            score += 1
                            fuzzy_matches.append(f"{kw}~{title_score}")
                        elif summary_match:
                            keywords_matched += 1
                            matched_keywords.add(kw)
                            score += 0.5
                            fuzzy_matches.append(f"{kw}~{summary_score}")

                # Skip if not all keywords matched in AND mode
                if keywords_matched < len(query_keywords):
                    continue

            else:  # OR mode
                # OR mode: any keyword match is good
                if exact_matches:
                    matched_keywords.update(exact_matches)
                    score += len(exact_matches) * 2

                # Try fuzzy for unmatched keywords
                if use_fuzzy and FUZZY_AVAILABLE:
                    for kw in query_keywords - exact_matches:
                        title_match, title_score = fuzzy_match(doc.get('title', ''), {kw})
                        summary_match, summary_score = fuzzy_match(doc.get('summary', ''), {kw})

                        if title_match:
                            matched_keywords.add(kw)
                            score += 1
                            fuzzy_matches.append(f"{kw}~{title_score}")
                        elif summary_match:
                            matched_keywords.add(kw)
                            score += 0.5
                            fuzzy_matches.append(f"{kw}~{summary_score}")

                # Skip if no matches at all in OR mode
                if not matched_keywords:
                    continue

            # Boost score for title matches
            if query_keywords & title_words:
                score += 3

            # Add to results
            if score > 0:
                results.append({
                    'doc': doc,
                    'cluster': cluster_name,
                    'score': score,
                    'matched_keywords': matched_keywords,
                    'fuzzy_matches': fuzzy_matches
                })

    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def format_result(result: Dict, index: Optional[int] = None) -> str:
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
    output.append(f"   🏷️  Cluster: {cluster} | Urgency: {urgency.upper()} | Score: {score:.1f}")

    # Show matched keywords
    if result.get('matched_keywords'):
        keywords_str = ', '.join(sorted(result['matched_keywords']))
        output.append(f"   🔍 Matched: {keywords_str}")

    # Show fuzzy matches if any
    if result.get('fuzzy_matches'):
        fuzzy_str = ', '.join(result['fuzzy_matches'])
        output.append(f"   🎯 Fuzzy: {fuzzy_str}")

    return '\n'.join(output)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='DEIA Librarian - Query the Global Commons index',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "DNS not working"
  %(prog)s "deployment failed" --urgency critical
  %(prog)s "python encoding" --platform windows
  %(prog)s "coordination" AND "governance"
  %(prog)s "deployment" OR "release" --audience advanced
  %(prog)s "pyhton" --fuzzy  # typo tolerance
        """
    )

    parser.add_argument('query', nargs='+', help='Search query (use AND/OR for logic)')
    parser.add_argument('--urgency', choices=['critical', 'high', 'medium', 'low'],
                        help='Filter by urgency level')
    parser.add_argument('--platform', help='Filter by platform (e.g., netlify, windows)')
    parser.add_argument('--audience', choices=['beginner', 'intermediate', 'advanced'],
                        help='Filter by audience level')
    parser.add_argument('--no-fuzzy', action='store_true',
                        help='Disable fuzzy matching (enabled by default)')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT,
                        help=f'Number of results to show (default: {DEFAULT_LIMIT})')

    return parser.parse_args()


def main():
    """Main CLI entry point"""
    args = parse_args()

    # Parse query for AND/OR logic
    query_parts = args.query
    logic_mode = "AND"  # default

    # Detect AND/OR in query
    if "AND" in query_parts:
        logic_mode = "AND"
        query_parts = [p for p in query_parts if p != "AND"]
    elif "OR" in query_parts:
        logic_mode = "OR"
        query_parts = [p for p in query_parts if p != "OR"]

    query_str = ' '.join(query_parts)

    # Load index
    print("Loading index...")
    index = load_index()
    print(f"Loaded {index.get('total_documents', 0)} documents in {index.get('total_clusters', 0)} clusters\n")

    # Display search parameters
    print(f"Query: \"{query_str}\"")
    print(f"Logic: {logic_mode}")

    filters = {}
    if args.urgency:
        print(f"Urgency filter: {args.urgency}")
        filters['urgency'] = args.urgency
    if args.platform:
        print(f"Platform filter: {args.platform}")
        filters['platform'] = args.platform
    if args.audience:
        print(f"Audience filter: {args.audience}")
        filters['audience'] = args.audience

    use_fuzzy = not args.no_fuzzy and FUZZY_AVAILABLE
    print(f"Fuzzy matching: {'enabled' if use_fuzzy else 'disabled'}")
    print("\n" + "=" * 70)

    # Extract keywords and search
    keywords = extract_keywords(query_str)
    print(f"Keywords: {', '.join(sorted(keywords))}\n")

    results = search_index(
        index,
        keywords,
        logic_mode=logic_mode,
        urgency_filter=args.urgency,
        platform_filter=args.platform,
        audience_filter=args.audience,
        use_fuzzy=use_fuzzy
    )

    # Log query for usage tracking
    log_query(query_str, filters, len(results), logic_mode)

    # Display results
    if not results:
        print("\n❌ No matching documents found.")
        print("\nTry:")
        print("  - Broader keywords")
        print("  - OR logic instead of AND")
        print("  - Remove filters")
        if args.no_fuzzy:
            print("  - Enable fuzzy matching (remove --no-fuzzy)")
    else:
        print(f"\n✅ Found {len(results)} matching document(s):\n")
        for i, result in enumerate(results[:args.limit], 1):
            print(format_result(result, i))

        if len(results) > args.limit:
            print(f"\n... and {len(results) - args.limit} more. Use --limit to see more.")

    print("\n" + "=" * 70)
    print(f"\n💡 Index version: {index.get('version', 'unknown')}")
    print(f"   Last updated: {index.get('last_updated', 'unknown')}")
    print(f"   Usage log: {USAGE_LOG_PATH}")


if __name__ == '__main__':
    main()
