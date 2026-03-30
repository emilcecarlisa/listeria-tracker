#!/usr/bin/env python3
"""
FSIS Listeria Recalls Scraper
Scrapes detailed recall information from FSIS website for Listeria recalls in FY2025 (Oct 2024 - Sep 2025)

Requirements:
  pip install selenium beautifulsoup4 pandas requests

Usage:
  python3 scrapeFsisRecalls.py
"""

import time
import json
import pandas as pd
from datetime import datetime
import re

def scrape_with_selenium():
    """Scrape using Selenium (handles JavaScript rendering)"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from bs4 import BeautifulSoup

        print("=== FSIS Listeria Recalls Scraper ===\n")
        print("Setting up headless browser...")

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        driver = webdriver.Chrome(options=chrome_options)

        all_recalls = []
        page = 0

        while True:
            url = f"https://www.fsis.usda.gov/recalls?keywords=listeria&f%5B0%5D=year%3A606&f%5B1%5D=year%3A684&page={page}"
            print(f"\nFetching page {page + 1}...")
            driver.get(url)

            # Wait for recalls to load
            time.sleep(5)

            # Parse the rendered page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find recall articles/cards
            recalls = soup.find_all(['article', 'div'], class_=lambda x: x and ('recall' in str(x).lower() or 'card' in str(x).lower()))

            if not recalls:
                # Try alternative selectors
                recalls = soup.find_all('div', attrs={'data-history-node-id': True})

            print(f"  Found {len(recalls)} recalls on this page")

            if len(recalls) == 0:
                break

            for recall in recalls:
                recall_data = extract_recall_info(recall, soup)
                if recall_data and recall_data.get('title'):
                    all_recalls.append(recall_data)
                    print(f"  ✓ {recall_data.get('title', 'Unknown')[:60]}...")

            # Check if there's a next page
            next_button = soup.find('a', string=re.compile('Next', re.I)) or soup.find('a', rel='next')
            if not next_button:
                break

            page += 1

            # Safety limit
            if page >= 10:
                print("  Reached page limit (10 pages)")
                break

        driver.quit()
        print(f"\n✓ Scraped {len(all_recalls)} total recalls")
        return all_recalls

    except ImportError:
        print("ERROR: Selenium not installed")
        print("Install with: pip install selenium")
        print("\nYou also need Chrome/Chromium installed and chromedriver")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_recall_info(recall_element, full_soup):
    """Extract structured data from a recall element"""
    data = {}

    try:
        # Get full text
        text = recall_element.get_text(separator=' ', strip=True)

        # Title/Company
        title_elem = recall_element.find(['h2', 'h3', 'h4', 'a'])
        if title_elem:
            data['title'] = title_elem.get_text(strip=True)

        # Link to full recall page
        link_elem = recall_element.find('a', href=True)
        if link_elem:
            href = link_elem.get('href')
            if href.startswith('/'):
                href = 'https://www.fsis.usda.gov' + href
            data['url'] = href

        # Date (various formats)
        date_patterns = [
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}',
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}'
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, text)
            if date_match:
                data['recall_date'] = date_match.group(0)
                break

        # Establishment number
        est_patterns = [
            r'Est[ablishment]*\s*[#:.]?\s*([A-Z0-9\-+]+)',
            r'Establishment\s+Number:\s*([A-Z0-9\-+]+)',
            r'P-?(\d{4,5})',  # Common pattern P-####
            r'M-?(\d{4,5})'   # Common pattern M-####
        ]
        for pattern in est_patterns:
            est_match = re.search(pattern, text, re.IGNORECASE)
            if est_match:
                data['establishment_number'] = est_match.group(1)
                break

        # Pounds recalled
        pounds_patterns = [
            r'([\d,]+)\s*pounds?',
            r'([\d,]+)\s*lbs?'
        ]
        for pattern in pounds_patterns:
            pounds_match = re.search(pattern, text, re.IGNORECASE)
            if pounds_match:
                data['pounds_recalled'] = pounds_match.group(1).replace(',', '')
                break

        # Class (I, II, III)
        class_match = re.search(r'Class\s+(I{1,3})', text, re.IGNORECASE)
        if class_match:
            data['recall_class'] = class_match.group(1)

        # Reason (should contain Listeria)
        if 'listeria monocytogenes' in text.lower():
            data['reason'] = 'Listeria monocytogenes'
        elif 'listeria' in text.lower():
            data['reason'] = 'Listeria'

        # Product description (try to extract)
        if 'product' in text.lower():
            product_match = re.search(r'Product[s]?:\s*([^.]{10,200})', text, re.IGNORECASE)
            if product_match:
                data['product_description'] = product_match.group(1).strip()

        # Extract full text snippet
        data['text_snippet'] = text[:300]

    except Exception as e:
        print(f"    Error extracting recall info: {e}")

    return data


def scrape_without_selenium():
    """Fallback: Try to scrape without Selenium (limited - won't get JS-loaded content)"""
    import requests
    from bs4 import BeautifulSoup

    print("=== FSIS Listeria Recalls Scraper (No JS) ===\n")
    print("⚠️  This method may not capture all recalls (page uses JavaScript)")
    print("    For complete results, install Selenium\n")

    url = "https://www.fsis.usda.gov/recalls?keywords=listeria&f%5B0%5D=year%3A606&f%5B1%5D=year%3A684"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    print("Fetching page...")
    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"ERROR: HTTP {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find recall links in the static HTML
    links = soup.find_all('a', href=lambda x: x and '/recall-case' in str(x))

    print(f"Found {len(links)} recall case links\n")

    recalls = []
    for link in links[:20]:  # Limit to first 20
        href = link.get('href')
        if href.startswith('/'):
            href = 'https://www.fsis.usda.gov' + href

        title = link.get_text(strip=True)
        recalls.append({
            'title': title,
            'url': href
        })
        print(f"  ✓ {title[:60]}...")

    return recalls


def save_results(recalls, output_dir='../data'):
    """Save scraped recalls to CSV and JSON"""
    if not recalls:
        print("\n⚠️  No recalls to save")
        return

    df = pd.DataFrame(recalls)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save as CSV
    csv_path = f'{output_dir}/fsisListeriaRecalls_FY2025_{timestamp}.csv'
    df.to_csv(csv_path, index=False)
    print(f"\n✓ Saved CSV: {csv_path}")

    # Save as JSON
    json_path = f'{output_dir}/fsisListeriaRecalls_FY2025_{timestamp}.json'
    with open(json_path, 'w') as f:
        json.dump(recalls, f, indent=2)
    print(f"✓ Saved JSON: {json_path}")

    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total recalls scraped: {len(recalls)}")
    print(f"\nColumns: {list(df.columns)}")

    if 'recall_date' in df.columns:
        print(f"\nDate range: {df['recall_date'].min()} to {df['recall_date'].max()}")

    if 'establishment_number' in df.columns:
        unique_est = df['establishment_number'].nunique()
        print(f"Unique establishments: {unique_est}")

    if 'pounds_recalled' in df.columns:
        total_pounds = pd.to_numeric(df['pounds_recalled'], errors='coerce').sum()
        print(f"Total pounds recalled: {total_pounds:,.0f}")

    print(f"{'='*80}")

    return csv_path, json_path


if __name__ == '__main__':
    # Try Selenium first
    recalls = scrape_with_selenium()

    # Fallback to non-JS version
    if recalls is None:
        print("\nFalling back to non-JavaScript scraping...")
        recalls = scrape_without_selenium()

    # Save results
    if recalls:
        save_results(recalls)
    else:
        print("\n❌ No recalls scraped")
        print("\nTroubleshooting:")
        print("  1. Install selenium: pip install selenium")
        print("  2. Install Chrome/Chromium browser")
        print("  3. Install chromedriver (brew install chromedriver on Mac)")
        print("  4. Or manually visit: https://www.fsis.usda.gov/recalls?keywords=listeria&f%5B0%5D=year%3A606&f%5B1%5D=year%3A684")
