#!/usr/bin/env python3
"""
Test script to verify FSIS API connectivity and response format

This makes a small test request to ensure:
1. The API endpoint is correct
2. The response format matches expectations
3. We can parse the data correctly
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fsisApi.client import FSISAPIClient
from fsisApi.filters import RecallFilters


def testApiRequest():
    """Make a test API request and display results"""

    print("=" * 80)
    print("FSIS API TEST - Verifying Connectivity and Response Format")
    print("=" * 80)

    # Create client
    client = FSISAPIClient()

    # Test with a small query: Listeria recalls from 2024
    print("\nTest Query: Listeria recalls from 2024")
    filters = RecallFilters.yearAndPathogen(year=2024, pathogen='listeria')
    print(f"Filters: {filters}")

    try:
        # Fetch data
        print("\nMaking API request...")
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
            print(f"Record type: {type(firstRecord)}")
            print(f"Number of fields: {len(firstRecord) if isinstance(firstRecord, dict) else 'N/A'}")

            if isinstance(firstRecord, dict):
                print(f"\nAvailable fields:")
                for i, key in enumerate(sorted(firstRecord.keys()), 1):
                    valuePreview = str(firstRecord[key])[:60]
                    if len(str(firstRecord[key])) > 60:
                        valuePreview += "..."
                    print(f"  {i:2d}. {key:35s} = {valuePreview}")

                print(f"\n--- Full First Record (JSON) ---")
                print(json.dumps(firstRecord, indent=2)[:1500])
                if len(json.dumps(firstRecord)) > 1500:
                    print("... (truncated)")

            # Check for key fields we need
            print(f"\n--- Key Field Verification ---")
            expectedFields = [
                'field_recall_number',
                'field_establishment',
                'field_year',
                'field_summary',
                'field_recall_reason',
                'field_product_items',
                'field_recall_classification',
                'field_closed_date',
                'field_states',
                'field_related_to_outbreak'
            ]

            for field in expectedFields:
                status = "✓" if field in firstRecord else "✗"
                value = firstRecord.get(field, 'N/A')
                valuePreview = str(value)[:50]
                if len(str(value)) > 50:
                    valuePreview += "..."
                print(f"  {status} {field:35s} = {valuePreview}")

        elif isinstance(data, list) and len(data) == 0:
            print("\n⚠️  API returned empty list (no recalls found with these filters)")
            print("This could mean:")
            print("  1. The filter parameters need adjustment")
            print("  2. No recalls exist for this query")
            print("  3. The API field names might be different")

        else:
            print(f"\n⚠️  Unexpected response format")
            print(f"Response: {str(data)[:500]}")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)

        # Save full response for inspection
        outputFile = Path(__file__).parent.parent / 'data' / 'testApiResponse.json'
        with open(outputFile, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Full response saved to: {outputFile}")

        return data

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        client.close()


if __name__ == '__main__':
    testApiRequest()
