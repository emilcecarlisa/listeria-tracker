"""
Selenium-based FSIS API Client - Bypasses Akamai bot protection
"""

import json
import time
from typing import Dict, Any, List
from urllib.parse import urlencode


class SeleniumAPIClient:
    """Client that uses Selenium to bypass bot protection"""

    BASE_URL = "https://www.fsis.usda.gov/fsis/api/recall/v/1"

    def __init__(self, headless: bool = False):
        """
        Initialize Selenium client

        Args:
            headless: Run browser in headless mode (may be blocked by bot protection)
        """
        self.driver = None
        self.headless = headless
        self.sessionEstablished = False

    def _initDriver(self):
        """Initialize Chrome driver"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            chromeOptions = Options()

            if self.headless:
                chromeOptions.add_argument('--headless')
                print("⚠️  Using headless mode (may be detected by bot protection)")
            else:
                print("Using visible browser window")

            chromeOptions.add_argument('--no-sandbox')
            chromeOptions.add_argument('--disable-dev-shm-usage')
            chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
            chromeOptions.add_argument('--window-size=1920,1080')
            chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
            chromeOptions.add_experimental_option('useAutomationExtension', False)

            self.driver = webdriver.Chrome(options=chromeOptions)

            # Hide webdriver detection
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })

            print("✓ Selenium Chrome driver initialized")

        except ImportError:
            raise ImportError(
                "Selenium not installed. Install with: pip install selenium"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Chrome driver: {e}\n"
                "Make sure Chrome/Chromium and chromedriver are installed."
            )

    def fetchRecalls(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch recalls using Selenium

        Args:
            params: Query parameters

        Returns:
            List of recall records
        """
        if not self.driver:
            self._initDriver()

        # Establish session by visiting main recalls page first
        if not self.sessionEstablished:
            print("Establishing session by visiting recalls page...")
            self.driver.get('https://www.fsis.usda.gov/recalls')
            time.sleep(5)  # Wait for cookies/session
            self.sessionEstablished = True
            print("✓ Session established")

        # Build URL
        url = self._buildUrl(params)
        print(f"Fetching: {url}")

        try:
            # Navigate to API endpoint
            self.driver.get(url)

            # Wait a bit for page to load
            time.sleep(3)

            # Get page source (which should be JSON)
            pageSource = self.driver.page_source

            # Extract JSON from <pre> tags (Firefox/Chrome display JSON in <pre>)
            if '<pre>' in pageSource:
                jsonStart = pageSource.find('<pre>') + 5
                jsonEnd = pageSource.find('</pre>')
                jsonText = pageSource[jsonStart:jsonEnd]
            elif '<body>' in pageSource:
                # Some browsers wrap JSON in body
                jsonStart = pageSource.find('<body>') + 6
                jsonEnd = pageSource.find('</body>')
                jsonText = pageSource[jsonStart:jsonEnd]
            else:
                # Raw JSON
                jsonText = pageSource

            # Parse JSON
            data = json.loads(jsonText)

            print(f"✓ Received {len(data) if isinstance(data, list) else 'unknown'} records")

            return data

        except json.JSONDecodeError as e:
            print(f"✗ JSON Parse Error: {e}")
            print(f"Page content preview: {pageSource[:500]}")
            raise

        except Exception as e:
            print(f"✗ Error: {e}")
            raise

    def _buildUrl(self, params: Dict[str, Any]) -> str:
        """Build full URL with query parameters"""
        if not params:
            return self.BASE_URL

        queryString = urlencode(params)
        return f"{self.BASE_URL}?{queryString}"

    def close(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
            print("✓ Selenium driver closed")
