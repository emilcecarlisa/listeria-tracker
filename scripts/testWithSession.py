#!/usr/bin/env python3
"""
Test API access by establishing a browser session first
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import cloudscraper
    print("Using cloudscraper...")
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'darwin', 'desktop': True}
    )
except ImportError:
    import requests
    print("Using requests...")
    scraper = requests.Session()
    scraper.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

# Step 1: Visit the recalls page to establish session/cookies
print("\nStep 1: Visiting recalls page to get cookies...")
response1 = scraper.get('https://www.fsis.usda.gov/recalls', timeout=30)
print(f"Status: {response1.status_code}")
print(f"Cookies: {len(response1.cookies)} cookies received")

# Step 2: Make API request with the established session
print("\nStep 2: Making API request with session cookies...")
api_url = 'https://www.fsis.usda.gov/fsis/api/recall/v/1?field_year_id=606&field_summary_value=listeria'
response2 = scraper.get(api_url, timeout=30)
print(f"Status: {response2.status_code}")

if response2.status_code == 200:
    data = response2.json()
    print(f"\n✓ SUCCESS! Received {len(data)} records")
    if len(data) > 0:
        print(f"\nFirst record keys: {list(data[0].keys())[:10]}")
else:
    print(f"\n✗ Failed: {response2.text[:200]}")
