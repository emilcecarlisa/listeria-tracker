# USDA FSIS Recall API Client

Backend service for fetching meat recall data from the USDA FSIS Recall API.

## Features

- ✅ Fetches recall data for 2024 and 2025
- ✅ Searches for specific pathogens (Listeria, Salmonella)
- ✅ Bypasses Akamai bot protection using Selenium
- ✅ Parses and normalizes API responses
- ✅ Deduplicates expansion recalls
- ✅ Exports to JSON and CSV formats
- ✅ Atomic functions with separation of concerns

## Architecture

```
fsisApi/
├── client.py           # HTTP API client (requests/cloudscraper)
├── seleniumClient.py   # Selenium-based client (bypasses bot protection) ⭐
├── filters.py          # Query parameter builders
├── parsers.py          # Response parsing & data normalization
├── storage.py          # Data persistence (JSON/CSV)
└── README.md

scripts/
├── fetchFsisRecalls.py  # Main script - fetches all data
├── testSeleniumApi.py   # Test API connectivity
└── testWithSession.py   # Debug script
```

## Installation

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install selenium cloudscraper requests

# Install ChromeDriver (macOS)
brew install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

## Usage

### Fetch All Recalls (2024-2025, Listeria + Salmonella)

```bash
python scripts/fetchFsisRecalls.py
```

**Output files:**
- `data/recalls2024Listeria.json` - 2024 Listeria recalls
- `data/recalls2024Salmonella.json` - 2024 Salmonella recalls
- `data/recalls2025Listeria.json` - 2025 Listeria recalls
- `data/recalls2025Salmonella.json` - 2025 Salmonella recalls
- `data/recallsAllCombined.json` - All recalls (deduplicated)
- `data/recallsAllCombined.csv` - All recalls in CSV format

### Run in Headless Mode (may be blocked)

```bash
python scripts/fetchFsisRecalls.py --headless
```

### Test API Connectivity

```bash
python scripts/testSeleniumApi.py
```

## API Details

**Base URL:** `https://www.fsis.usda.gov/fsis/api/recall/v/1`

**Key Parameters:**
- `field_year_id` - Year taxonomy ID (2024=606, 2025=684)
- `field_summary_value` - Text search in summary (e.g., "listeria", "salmonella")

**Bot Protection:**
- The API uses Akamai CDN with aggressive bot protection
- Standard HTTP requests (requests, curl) return 403 Forbidden
- **Solution:** Selenium with visible browser window + session establishment

## Parsed Data Fields

Each recall record includes:

```json
{
  "recallNumber": "030-2024-EXP",
  "recallClass": "Class I",
  "riskLevel": "High - Class I",
  "establishment": "Yushang Food Inc.",
  "title": "Yu Shang Food, Inc. Recalls Ready-To-Eat Meat...",
  "processingCategory": "Fully Cooked - Not Shelf Stable",
  "recallReason": "Product Contamination",
  "poundsRecovered": 60020,
  "recallDate": "2024-11-21",
  "closedDate": "2025-04-15",
  "year": "2024",
  "states": "",
  "relatedToOutbreak": true,
  "isArchived": true,
  "summary": "...",
  "recallUrl": "http://www.fsis.usda.gov/recalls-alerts/...",
  "language": "English"
}
```

## Programmatic Usage

```python
from fsisApi.seleniumClient import SeleniumAPIClient
from fsisApi.filters import RecallFilters
from fsisApi.parsers import RecallParser
from fsisApi.storage import RecallStorage

# Initialize client
client = SeleniumAPIClient(headless=False)

# Build filters
filters = RecallFilters.yearAndPathogen(year=2024, pathogen='listeria')

# Fetch data
rawRecalls = client.fetchRecalls(filters)

# Parse data
parsedRecalls = RecallParser.parseMultiple(rawRecalls)

# Save data
RecallStorage.saveToJson(parsedRecalls, 'output.json')

# Close browser
client.close()
```

## Deduplication

Recalls can have expansions (e.g., `030-2024` and `030-2024-EXP`). The system:
1. Groups recalls by base number
2. Prefers expansion versions (most complete)
3. Removes duplicate entries

## API Documentation

See: `docs/Recall-API-documentation.pdf`

## Troubleshooting

### 403 Forbidden Errors

The API has Akamai bot protection. Solutions:
- ✅ Use `SeleniumAPIClient` (recommended)
- ✅ Run with visible browser (`headless=False`)
- ❌ Standard HTTP clients won't work

### Chrome/ChromeDriver Issues

```bash
# macOS: Allow chromedriver to run
xattr -d com.apple.quarantine /usr/local/bin/chromedriver

# Or install via Homebrew
brew install --cask chromedriver
```

### No Data Returned

If `[]` is returned:
- Check year taxonomy IDs are correct
- Verify pathogen spelling
- Test in browser first

## Next Steps

For analysis, see:
- `analysis/recallAnalyzer.py` - Company recall rate analysis (to be implemented)
- `analysis/pathogenAnalyzer.py` - Pathogen comparison (to be implemented)
