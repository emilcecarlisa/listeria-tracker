"""
FSIS API Client - Handles HTTP requests to USDA FSIS Recall API
"""

import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode

import requests

try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False


class FSISAPIClient:
    """Client for USDA FSIS Recall API"""

    BASE_URL = "https://www.fsis.usda.gov/fsis/api/recall/v/1"

    def __init__(self, timeout: int = 30):
        """
        Initialize API client

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout

        if HAS_CLOUDSCRAPER:
            # Use cloudscraper to bypass Akamai bot protection
            self.session = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'darwin',
                    'desktop': True
                }
            )
            print("Using cloudscraper for bot protection bypass")
        else:
            # Fallback to requests with enhanced headers
            import requests
            self.session = requests.Session()
            print("⚠️  cloudscraper not available, using requests (may encounter 403 errors)")

        self.session.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.fsis.usda.gov/recalls',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })

    def fetchRecalls(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch recalls from FSIS API

        Args:
            params: Query parameters (e.g., {'field_year_id': '2024', 'field_summary_value': 'listeria'})

        Returns:
            JSON response as dict

        Raises:
            requests.RequestException: If request fails
        """
        # Build full URL
        url = self._buildUrl(params)

        print(f"Fetching: {url}")

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            print(f"✓ Received {len(data) if isinstance(data, list) else 'unknown'} records")

            return data

        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Error: {e}")
            print(f"  Response: {e.response.text[:200]}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"✗ Request Error: {e}")
            raise
        except ValueError as e:
            print(f"✗ JSON Parse Error: {e}")
            raise

    def _buildUrl(self, params: Dict[str, Any]) -> str:
        """Build full URL with query parameters"""
        if not params:
            return self.BASE_URL

        query_string = urlencode(params)
        return f"{self.BASE_URL}?{query_string}"

    def close(self):
        """Close HTTP session"""
        self.session.close()
