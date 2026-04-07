#!/usr/bin/env python3
"""
Test FSIS API using Selenium (bypasses Akamai bot protection)
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fsisApi.seleniumClient import SeleniumAPIClient
from fsisApi.filters import RecallFilters


def testSeleniumApi():
    """Test API access using Selenium"""

    print("=" * 80)
    print("FSIS API TEST - Using Selenium to Bypass Bot Protection")
    print("=" * 80)

    # Use visible browser (not headless) to avoid detection
    client = SeleniumAPIClient(headless=False)

    # Test with Listeria recalls from 2024
    print("\nTest Query: Listeria recalls from 2024")
    filters = RecallFilters.yearAndPathogen(year=2024, pathogen='listeria')
    print(f"Filters: {filters}")

    try:
        print("\nInitializing Selenium and fetching data...")
        data = client.fetchRecalls(filters)

        # Analyze response
        print("\n" + "=" * 80)
        print("RESPONSE ANALYSIS")
        print("=" * 80)

        print(f"\nResponse Type: {type(data)}")
        print(f"Number of records: {len(data) if isinstance(data, list) else 'N/A'}")

        if isinstance(data, list) and len(data) > 0:
            print(f"\n--- First Record ---")
            firstRecord = data[0]
            print(f"Number of fields: {len(firstRecord) if isinstance(firstRecord, dict) else 'N/A'}")

            if isinstance(firstRecord, dict):
                print(f"\nAvailable fields:")
                for i, key in enumerate(sorted(firstRecord.keys()), 1):
                    valuePreview = str(firstRecord[key])[:60]
                    if len(str(firstRecord[key])) > 60:
                        valuePreview += "..."
                    print(f"  {i:2d}. {key:35s} = {valuePreview}")

        elif isinstance(data, list) and len(data) == 0:
            print("\n⚠️  API returned empty list")
            print("This could mean:")
            print("  1. No recalls exist matching these filters")
            print("  2. The filter values might need adjustment")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)

        # Save response
        outputFile = Path(__file__).parent.parent / 'data' / 'testSeleniumApiResponse.json'
        with open(outputFile, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Response saved to: {outputFile}")

        return data

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        client.close()


if __name__ == '__main__':
    testSeleniumApi()
