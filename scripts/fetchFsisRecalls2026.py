#!/usr/bin/env python3
"""
Fetch USDA FSIS Recall Data for 2026 ONLY

Fetches recall data for:
- Year: 2026 (taxonomy ID: 685)
- Pathogens: Listeria, Salmonella

Note: FSIS API 'year' taxonomy does NOT equal calendar year.
      year=2026 captures Nov-Dec 2025 + early 2026 recalls

This script only fetches 2026 data and merges with existing 2024-2025 data.
"""

import sys
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from fsisApi.seleniumClient import SeleniumAPIClient
from fsisApi.filters import RecallFilters
from fsisApi.parsers import RecallParser
from fsisApi.storage import RecallStorage


def fetch2026Recalls(headless: bool = False):
    """
    Fetch 2026 recall data and merge with existing data

    Args:
        headless: Run browser in headless mode (may be blocked)
    """
    print("=" * 80)
    print("USDA FSIS RECALL DATA FETCHER - 2026 ONLY")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Verify 2026 taxonomy ID
    if 2026 not in RecallFilters.YEAR_IDS:
        print("✗ Year 2026 not found in taxonomy mapping!")
        return

    print(f"✓ Year 2026 taxonomy ID verified: {RecallFilters.YEAR_IDS[2026]}")

    # Define queries for 2026 only
    queries = [
        {'year': 2026, 'pathogen': 'listeria', 'label': '2026 Listeria'},
        {'year': 2026, 'pathogen': 'salmonella', 'label': '2026 Salmonella'},
    ]

    # Initialize client
    client = SeleniumAPIClient(headless=headless)

    recalls2026Raw = []
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

                print(f"Filter parameters: {filters}")

                # Fetch data
                rawRecalls = client.fetchRecalls(filters)

                # Parse data
                parsedRecalls = RecallParser.parseMultiple(rawRecalls)

                # Store results
                resultsByQuery[query['label']] = parsedRecalls
                recalls2026Raw.extend(parsedRecalls)

                print(f"✓ Fetched {len(parsedRecalls)} recalls for {query['label']}")

                # Save individual file
                filename = f"recalls{query['year']}{query['pathogen'].title()}.json"
                filepath = Path(__file__).parent.parent / 'data' / filename
                RecallStorage.saveToJson(parsedRecalls, filepath)
                print(f"✓ Saved to {filepath}")

            except Exception as e:
                print(f"✗ Error fetching {query['label']}: {e}")
                import traceback
                traceback.print_exc()

        # Load existing 2024-2025 data
        print(f"\n{'=' * 80}")
        print("MERGING WITH EXISTING 2024-2025 DATA")
        print(f"{'=' * 80}")

        existingPath = Path(__file__).parent.parent / 'data' / 'recallsAllCombined.json'
        if existingPath.exists():
            with open(existingPath, 'r') as f:
                existing = json.load(f)
            print(f"✓ Loaded {len(existing)} existing recalls (2024-2025)")
        else:
            print("⚠️  No existing combined file found, starting fresh")
            existing = []

        # Combine all data
        allRecallsRaw = existing + recalls2026Raw
        print(f"Total records before deduplication: {len(allRecallsRaw)}")

        # Deduplicate
        allRecalls = RecallStorage.mergeDeduplicate(allRecallsRaw)
        print(f"After deduplication: {len(allRecalls)}")
        print(f"  New unique recalls from 2026: {len(allRecalls) - len(existing)}")

        # Save combined file
        combinedPath = Path(__file__).parent.parent / 'data' / 'recallsAllCombined.json'
        RecallStorage.saveToJson(allRecalls, combinedPath)
        print(f"✓ Saved combined data to {combinedPath}")

        # Save as CSV too
        csvPath = Path(__file__).parent.parent / 'data' / 'recallsAllCombined.csv'
        RecallStorage.saveToCsv(allRecalls, csvPath)
        print(f"✓ Saved CSV to {csvPath}")

        # Print summary
        print(f"\n{'=' * 80}")
        print("SUMMARY")
        print(f"{'=' * 80}")

        print(f"\nNew 2026 data:")
        for label, recalls in resultsByQuery.items():
            print(f"  {label:20s}: {len(recalls):3d} recalls")

        print(f"\n  {'Total 2026 raw':20s}: {len(recalls2026Raw):3d} recalls")

        # Analyze combined dataset by year
        print(f"\nCombined dataset (all years):")
        print(f"  Total (deduplicated): {len(allRecalls)} recalls")

        # Count by year
        from collections import Counter
        yearCounts = Counter(r.get('year') for r in allRecalls)
        for year in sorted(yearCounts.keys()):
            print(f"    {year}: {yearCounts[year]} recalls")

        # Analyze 2026 date range
        recalls2026 = [r for r in allRecalls if r.get('year') == '2026']
        if recalls2026:
            dates = [r.get('recallDate') for r in recalls2026 if r.get('recallDate')]
            if dates:
                print(f"\n  2026 date range: {min(dates)} to {max(dates)}")

        # Analyze by pathogen
        listeriaCount = sum(1 for r in allRecalls if 'listeria' in r.get('summary', '').lower())
        salmonellaCount = sum(1 for r in allRecalls if 'salmonella' in r.get('summary', '').lower())

        print(f"\nBy pathogen (all years):")
        print(f"  Listeria:   {listeriaCount:3d} recalls")
        print(f"  Salmonella: {salmonellaCount:3d} recalls")

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
        description='Fetch USDA FSIS recall data for 2026 and merge with existing'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (may be detected by bot protection)'
    )

    args = parser.parse_args()

    fetch2026Recalls(headless=args.headless)
