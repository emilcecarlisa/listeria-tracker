# Fetch 2026 Recall Data - Instructions

## Background

### FSIS API Year Taxonomy Issue

The FSIS API's "year" parameter **does NOT correspond to calendar years**:

| API Year | Taxonomy ID | Actual Recalls Covered |
|----------|-------------|------------------------|
| 2024 | 606 | Jan 2024 - Nov 2024 |
| 2025 | 684 | May 2025 - Oct 2025 |
| **2026** | **685** | **Nov-Dec 2025 + early 2026** |

**Problem:** When we fetched `year=2025`, we only got recalls through October 2025, missing Nov-Dec 2025.

**Solution:** Fetch `year=2026` to capture the missing Nov-Dec 2025 recalls.

## Current Data Status

**What we have:**
- ✅ 2024 recalls: Jan - Nov 2024
- ✅ 2025 recalls: May - Oct 2025
- ❌ **Missing: Nov-Dec 2025** (~5 months ago when last fetched)

**What we need:**
- Fetch `year=2026` (taxonomy ID: 685)
- This will capture Nov-Dec 2025 + any early 2026 recalls

## How to Fetch 2026 Data

### Step 1: Verify Taxonomy ID

The script automatically verifies that 2026 has the correct taxonomy ID (685):

```python
from fsisApi.filters import RecallFilters
print(RecallFilters.YEAR_IDS[2026])  # Should print: 685
```

### Step 2: Run Fetch Script

**Note:** This requires Selenium and a visible browser (Akamai bot protection).

```bash
# Activate virtual environment
source .venv/bin/activate

# Run fetch script (browser will open)
python scripts/fetchFsisRecalls2026.py
```

**What it does:**
1. Fetches 2026 Listeria recalls
2. Fetches 2026 Salmonella recalls
3. Loads existing 2024-2025 data
4. Merges and deduplicates
5. Saves to `data/recallsAllCombined.json` and `.csv`

**Expected output:**
```
✓ Year 2026 taxonomy ID verified: 685
✓ Fetched X recalls for 2026 Listeria
✓ Fetched X recalls for 2026 Salmonella
✓ Loaded 20 existing recalls (2024-2025)
Total records before deduplication: 20+X
After deduplication: Y
  New unique recalls from 2026: Y-20
```

### Step 3: Update Processed Data

After fetching new raw data, re-run data preparation:

```bash
cd scripts
python prepareDataForDashboard.py
```

This will:
- Reload `recallsAllCombined.csv` (now includes 2026 data)
- Derive pathogen categories
- Filter for FY2025 overlap period (Oct 2024 - Sep 2025)
- Regenerate `data/processed/` files

### Step 4: Update Dashboard

The dashboard will automatically pick up the new data when you re-run it:

```bash
cd visualizations
jupyter notebook comprehensiveDashboard2026.ipynb
```

## Expected Results

### Date Coverage After Fetching 2026

| Period | Lab Data | Recall Data | Status |
|--------|----------|-------------|--------|
| Jan-Sep 2024 | ❌ No data | ✅ Available | No overlap |
| Oct-Dec 2024 | ✅ Available | ✅ Available | ✓ **Overlap** |
| Jan-Sep 2025 | ✅ Available | ✅ Available | ✓ **Overlap** |
| Oct-Dec 2025 | ❌ Ended Sep 30 | ✅ **NEW from 2026 fetch** | No overlap |
| Jan-Apr 2026 | ❌ No data | ✅ **NEW from 2026 fetch** | No overlap |

### Improved Overlap

**Before:** 9 of 20 recalls (45%) aligned with lab data  
**After:** Potentially more recalls in FY2025 period (Oct 2024 - Sep 2025)

## Data Preparation Updates Needed

### Filter for FY2025 Alignment

Update `prepareDataForDashboard.py` to filter recalls by date range:

```python
# Filter recalls to FY2025 period (Oct 1, 2024 - Sep 30, 2025)
fy2025_start = pd.to_datetime('2024-10-01')
fy2025_end = pd.to_datetime('2025-09-30')

recallsDf_fy2025 = recallsDf[
    (recallsDf['recallDate'] >= fy2025_start) & 
    (recallsDf['recallDate'] <= fy2025_end)
].copy()

print(f"\nTemporal Alignment:")
print(f"  Total recalls: {len(recallsDf)}")
print(f"  In FY2025 period: {len(recallsDf_fy2025)}")
print(f"  Alignment rate: {len(recallsDf_fy2025)/len(recallsDf)*100:.1f}%")
```

### Dashboard Documentation Updates

Add temporal alignment disclaimer:

```markdown
## Data Alignment Note

**Lab Sampling Period:** FY2025 (Oct 1, 2024 - Sep 30, 2025)
**Recall Data Period:** Calendar 2024-2026 (Jan 2024 - present)

**Temporal Overlap:** Only recalls within FY2025 can be directly correlated 
with lab contamination data. Recalls outside this period are shown for 
context but cannot be linked to lab sampling results.
```

## Files Updated

### Created
- `scripts/fetchFsisRecalls2026.py` - New script to fetch 2026 only

### Will be Modified
- `data/recallsAllCombined.json` - Merged data including 2026
- `data/recallsAllCombined.csv` - CSV version
- `data/recalls2026Listeria.json` - Raw 2026 Listeria data
- `data/recalls2026Salmonella.json` - Raw 2026 Salmonella data

### Should be Updated
- `scripts/prepareDataForDashboard.py` - Add FY2025 filtering
- `visualizations/comprehensiveDashboard2026.ipynb` - Add temporal disclaimer

## Verification Commands

After fetching, verify the data:

```bash
# Check date ranges in combined data
python3 << 'EOF'
import pandas as pd
df = pd.read_csv('data/recallsAllCombined.csv')
df['recallDate'] = pd.to_datetime(df['recallDate'])

print(f"Total recalls: {len(df)}")
print(f"\nDate range:")
print(f"  Earliest: {df['recallDate'].min()}")
print(f"  Latest: {df['recallDate'].max()}")

print(f"\nRecalls by year:")
print(df.groupby(df['recallDate'].dt.year)['recallNumber'].count())

print(f"\nFY2025 overlap (Oct 2024 - Sep 2025):")
fy2025 = df[(df['recallDate'] >= '2024-10-01') & (df['recallDate'] <= '2025-09-30')]
print(f"  {len(fy2025)} recalls ({len(fy2025)/len(df)*100:.1f}%)")
EOF
```

## Next Steps

1. ✅ Script created: `fetchFsisRecalls2026.py`
2. ⏳ **Run fetch** (requires Selenium, visible browser)
3. ⏳ **Update data prep** script to filter FY2025
4. ⏳ **Update dashboard** with temporal disclaimer
5. ⏳ **Verify** date alignment improved

---

**Status:** Ready to fetch 2026 data  
**Last Updated:** April 7, 2026
