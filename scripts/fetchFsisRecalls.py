#!/usr/bin/env python3
"""
Fetch USDA FSIS Recall Data via API

Fetches recall data for:
- Years: 2024, 2025, 2026
- Pathogens: Listeria, Salmonella

Note: FSIS API 'year' taxonomy does NOT equal calendar year.
      year=2025 returns recalls through ~Oct 2025
      year=2026 needed to capture Nov-Dec 2025 recalls

Saves to:
- Combined JSON file with all recalls
- Separate JSON files by year/pathogen
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from fsisApi.seleniumClient import SeleniumAPIClient
from fsisApi.filters import RecallFilters
from fsisApi.parsers import RecallParser
from fsisApi.storage import RecallStorage


def fetchAllRecalls(headless: bool = False):
    """
    Fetch all recall combinations

    Args:
        headless: Run browser in headless mode (may be blocked)
    """
    print("=" * 80)
    print("USDA FSIS RECALL DATA FETCHER")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Define queries
    queries = [
        {'year': 2024, 'pathogen': 'listeria', 'label': '2024 Listeria'},
        {'year': 2024, 'pathogen': 'salmonella', 'label': '2024 Salmonella'},
        {'year': 2025, 'pathogen': 'listeria', 'label': '2025 Listeria'},
        {'year': 2025, 'pathogen': 'salmonella', 'label': '2025 Salmonella'},
        {'year': 2026, 'pathogen': 'listeria', 'label': '2026 Listeria'},
        {'year': 2026, 'pathogen': 'salmonella', 'label': '2026 Salmonella'},
    ]

    # Initialize client
    client = SeleniumAPIClient(headless=headless)

    allRecallsRaw = []
    resultsByQuery = {}

    try:
        # Fetch each query
        for query in queries:
            print(f"\n{'─' * 80}")
            print(f"Fetching: {query['label']}")
            print(f"{'─' * 80}")

            try:
                # Build filters
                filters = RecallFilters.yearAndPathogen(
                    year=query['year'],
                    pathogen=query['pathogen']
                )

                # Fetch data
                rawRecalls = client.fetchRecalls(filters)

                # Parse data
                parsedRecalls = RecallParser.parseMultiple(rawRecalls)

                # Store results
                resultsByQuery[query['label']] = parsedRecalls
                allRecallsRaw.extend(parsedRecalls)

                print(f"✓ Fetched {len(parsedRecalls)} recalls for {query['label']}")

                # Save individual file
                filename = f"recalls{query['year']}{query['pathogen'].title()}.json"
                filepath = Path(__file__).parent.parent / 'data' / filename
                RecallStorage.saveToJson(parsedRecalls, filepath)

            except Exception as e:
                print(f"✗ Error fetching {query['label']}: {e}")
                import traceback
                traceback.print_exc()

        # Deduplicate combined results
        print(f"\n{'=' * 80}")
        print("DEDUPLICATING & COMBINING RESULTS")
        print(f"{'=' * 80}")

        print(f"Total raw records: {len(allRecallsRaw)}")
        allRecalls = RecallStorage.mergeDeduplicate(allRecallsRaw)
        print(f"After deduplication: {len(allRecalls)}")

        # Save combined file
        combinedPath = Path(__file__).parent.parent / 'data' / 'recallsAllCombined.json'
        RecallStorage.saveToJson(allRecalls, combinedPath)

        # Save as CSV too
        csvPath = Path(__file__).parent.parent / 'data' / 'recallsAllCombined.csv'
        RecallStorage.saveToCsv(allRecalls, csvPath)

        # Print summary
        print(f"\n{'=' * 80}")
        print("SUMMARY")
        print(f"{'=' * 80}")

        for label, recalls in resultsByQuery.items():
            print(f"  {label:20s}: {len(recalls):3d} recalls")

        print(f"\n  {'Total (deduplicated)':20s}: {len(allRecalls):3d} recalls")

        # Analyze by pathogen
        listeriaCount = sum(1 for r in allRecalls if 'listeria' in r.get('summary', '').lower())
        salmonellaCount = sum(1 for r in allRecalls if 'salmonella' in r.get('summary', '').lower())

        print(f"\nBy pathogen:")
        print(f"  Listeria:   {listeriaCount:3d} recalls")
        print(f"  Salmonella: {salmonellaCount:3d} recalls")

        # Analyze by year
        recalls2024 = sum(1 for r in allRecalls if r.get('year') == '2024')
        recalls2025 = sum(1 for r in allRecalls if r.get('year') == '2025')

        print(f"\nBy year:")
        print(f"  2024: {recalls2024:3d} recalls")
        print(f"  2025: {recalls2025:3d} recalls")

        # Analyze by outbreak
        outbreakCount = sum(1 for r in allRecalls if r.get('relatedToOutbreak'))

        print(f"\nRelated to outbreak: {outbreakCount:3d} recalls")

        print(f"\n{'=' * 80}")
        print("FETCH COMPLETE")
        print(f"{'=' * 80}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return allRecalls

    finally:
        client.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Fetch USDA FSIS recall data for 2024-2025'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (may be detected by bot protection)'
    )

    args = parser.parse_args()

    fetchAllRecalls(headless=args.headless)
