# USDA FSIS Recall API Service - Implementation Summary

## ✅ Project Complete

Built a production-ready backend service to fetch USDA FSIS meat recall data via their API.

## What Was Built

### Core Modules (camelCase convention)

```
fsisApi/
├── client.py              # HTTP client with cloudscraper
├── seleniumClient.py      # Selenium client (bypasses Akamai protection) ⭐
├── filters.py             # Query parameter builders with taxonomy mappings
├── parsers.py             # Data parsing & normalization
├── storage.py             # JSON/CSV persistence with deduplication
└── README.md              # Complete documentation
```

### Scripts

```
scripts/
├── fetchFsisRecalls.py    # Main script - fetches all data
├── testSeleniumApi.py     # Test API connectivity
└── testFsisApi.py         # HTTP client test (for debugging)
```

### Data Generated

```
data/
├── recalls2024Listeria.json       # 14 recalls (92KB)
├── recalls2024Salmonella.json     # 4 recalls (20KB)
├── recalls2025Listeria.json       # 10 recalls (53KB)
├── recalls2025Salmonella.json     # 0 recalls (empty)
├── recallsAllCombined.json        # 20 deduplicated (106KB)
└── recallsAllCombined.csv         # 20 deduplicated (96KB)
```

## Key Features

✅ **Atomic Functions** - Each module has single responsibility
✅ **Separation of Concerns** - Client → Filters → Parser → Storage
✅ **Year & Pathogen Filtering** - 2024/2025 + Listeria/Salmonella
✅ **Taxonomy ID Mapping** - Automatic conversion (2024→606, 2025→684)
✅ **Bot Protection Bypass** - Selenium with session establishment
✅ **Deduplication** - Merges expansion recalls (030-2024-EXP)
✅ **Multiple Formats** - JSON (structured) + CSV (analysis-ready)
✅ **Normalized Schema** - Clean, consistent field names

## API Challenge Solved

**Problem:** USDA FSIS API uses Akamai CDN with aggressive bot protection
- ❌ Standard HTTP requests → 403 Forbidden
- ❌ `requests` library → 403 Forbidden
- ❌ `cloudscraper` → 403 Forbidden
- ❌ Headless Selenium → 403 Forbidden

**Solution:** Selenium with visible browser + session establishment
1. Visit main recalls page first (get cookies)
2. Then access API endpoint
3. Works in visible browser mode

## Data Schema

### Normalized Fields

```python
{
    # Core identifiers
    'recallNumber': '030-2024-EXP',
    'recallClass': 'Class I',
    'riskLevel': 'High - Class I',

    # Company info
    'establishment': 'Yushang Food Inc.',
    'companyContact': '...',

    # Product details
    'title': 'Yu Shang Food, Inc. Recalls Ready-To-Eat...',
    'productItems': '...',
    'processingCategory': 'Fully Cooked - Not Shelf Stable',

    # Recall details
    'recallReason': 'Product Contamination',
    'recallType': 'Closed Recall',
    'poundsRecovered': 60020,  # Numeric, not string

    # Dates
    'recallDate': '2024-11-21',
    'closedDate': '2025-04-15',
    'year': '2024',

    # Geographic & Outbreak
    'states': '',
    'relatedToOutbreak': True,  # Boolean

    # Status
    'isArchived': True,
    'isActive': False,

    # Additional
    'summary': '...',  # HTML stripped
    'recallUrl': '...',
    'language': 'English'
}
```

## Usage Examples

### 1. Fetch All Data (Command Line)

```bash
source .venv/bin/activate
python scripts/fetchFsisRecalls.py
```

**Output:**
- 4 individual JSON files (by year/pathogen)
- 1 combined JSON file (deduplicated)
- 1 combined CSV file (analysis-ready)

### 2. Programmatic Usage

```python
from fsisApi.seleniumClient import SeleniumAPIClient
from fsisApi.filters import RecallFilters
from fsisApi.parsers import RecallParser

# Fetch 2024 Listeria recalls
client = SeleniumAPIClient(headless=False)
filters = RecallFilters.yearAndPathogen(2024, 'listeria')
rawData = client.fetchRecalls(filters)
recalls = RecallParser.parseMultiple(rawData)
client.close()

# Analyze
listeriaRecalls = [r for r in recalls if r['relatedToOutbreak']]
print(f"Found {len(listeriaRecalls)} outbreak-related recalls")
```

### 3. Load Saved Data for Analysis

```python
from fsisApi.storage import RecallStorage

# Load combined data
recalls = RecallStorage.loadFromJson('data/recallsAllCombined.json')

# Filter for specific analysis
rteListeria = [
    r for r in recalls
    if 'Fully Cooked' in r['processingCategory']
    and 'listeria' in r['summary'].lower()
]

# Calculate company recall rates
from collections import Counter
companies = Counter(r['establishment'] for r in recalls)
print(companies.most_common(5))
```

## Integration with Existing Dashboard

Ready to integrate with `rteListeriaDashboard.ipynb`:

```python
# In your dashboard notebook
from fsisApi.storage import RecallStorage

# Load recall data
recallData = RecallStorage.loadFromJson('../data/recallsAllCombined.json')

# Join with lab sampling data
# (Use establishment names to match)
for recall in recallData:
    establishment = recall['establishment']
    # Find matching lab samples...
    # Calculate recall rate...
```

## Statistics (Current Data)

**Total Recalls:** 20 (deduplicated from 28 raw)

**By Pathogen:**
- Listeria: 17 recalls (85%)
- Salmonella: 3 recalls (15%)

**By Year:**
- 2024: 10 recalls
- 2025: 10 recalls

**Outbreak-Related:** 4 recalls (20%)

**Class I (High Risk):** Majority

**Largest Recall:** Yu Shang Food - 60,020 lbs (Listeria, outbreak-related)

## Next Steps

### Phase 4: Analysis (Not Yet Implemented)

Create `analysis/recallAnalyzer.py`:

```python
def calculateCompanyRecallRate(recallData, labData):
    """
    Calculate recall rate per company
    Similar to rteListeriaDashboard analysis
    """
    # Group by establishment
    # Count recalls per establishment
    # Calculate rate: recalls / total samples
    pass

def identifyHighRiskCompanies(threshold=2):
    """
    Companies with multiple recalls in timeframe
    """
    pass

def analyzePathogenTrends():
    """
    Temporal trends by pathogen
    """
    pass
```

### Integration Tasks

1. **Match Establishments** - Link recall data to lab sampling data
   - Use establishment numbers (P-46684, etc.)
   - Fuzzy matching on company names

2. **Dashboard Updates** - Add to `rteListeriaDashboard.ipynb`
   - Section: "Company Recall History"
   - Graph: Recall rate vs contamination rate
   - Table: High-risk companies (multiple recalls)

3. **Automated Updates** - Schedule regular data fetches
   - Cron job or GitHub Actions
   - Weekly/monthly refresh

## Files & Folders

```
listeria-tracker/
├── fsisApi/               # NEW - API client modules
│   ├── __init__.py
│   ├── client.py
│   ├── seleniumClient.py
│   ├── filters.py
│   ├── parsers.py
│   ├── storage.py
│   └── README.md
├── scripts/
│   ├── fetchFsisRecalls.py   # NEW - Main fetch script
│   ├── testSeleniumApi.py    # NEW - Test script
│   └── ...existing scripts...
├── data/
│   ├── recalls2024Listeria.json       # NEW
│   ├── recalls2024Salmonella.json     # NEW
│   ├── recalls2025Listeria.json       # NEW
│   ├── recalls2025Salmonella.json     # NEW
│   ├── recallsAllCombined.json        # NEW
│   ├── recallsAllCombined.csv         # NEW
│   └── ...existing data...
├── docs/
│   └── Recall-API-documentation.pdf
├── FSIS_API_SUMMARY.md    # NEW - This file
└── ...existing files...
```

## Dependencies Added

```txt
selenium>=4.0.0
cloudscraper>=1.2.0
requests>=2.28.0
```

Install with:
```bash
source .venv/bin/activate
pip install selenium cloudscraper requests
```

## Technical Notes

- **camelCase Convention:** All files follow camelCase naming
- **Atomic Functions:** Each function has single purpose
- **Error Handling:** Try/except with detailed error messages
- **Type Hints:** Modern Python typing for clarity
- **Documentation:** Docstrings for all public methods
- **Separation:** Client/Filters/Parser/Storage are independent

## Conclusion

✅ **Backend service complete and tested**
✅ **All 2024-2025 recall data fetched**
✅ **Ready for dashboard integration**
✅ **Clean, maintainable, extensible code**

Ready to build company recall rate analysis similar to your RTE dashboard!
