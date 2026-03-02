# USDA FSIS Data Analysis Skill

**Purpose**: Guide analysis of USDA Food Safety and Inspection Service (FSIS) datasets, particularly focusing on pathogen detection, establishment inspections, and food safety data.

**Version**: 1.0
**Last Updated**: March 2, 2026

---

## Overview

This skill provides guidance for analyzing USDA FSIS data across multiple domains:
- **Laboratory Sampling Data**: Pathogen detection in food products
- **Good Commercial Practices (GCP) Data**: Animal welfare and handling inspections
- **Consumption Data**: USDA food intake surveys
- **Establishment Data**: Facility-level information

### User's Research Interests
- Correlating food popularity with contamination rates
- Establishment-level risk assessment
- Temporal trends in pathogen detection
- Multi-dataset integration and comparative analysis
- Food safety violations and animal welfare patterns

---

## Common Data Formats & Obstacles

### 1. USDA FSIS Excel Files (GCP Inspection Data)

**Format**: `.xlsx` files with metadata header rows

**Common Structure**:
```
Row 1: Metadata (e.g., "Data includes inspection tasks between October 1, 2023 - September 30, 2024")
Row 2: Additional metadata or blank
Row 3: Actual column headers (EstablishmentID, EstablishmentNumber, InspectionDate, etc.)
Row 4+: Data records
```

**Obstacle**: Pandas reads these files incorrectly by default, treating metadata rows as headers.

**Solution**:
```python
# Method 1: Skip metadata rows
df = pd.read_excel('file.xlsx', skiprows=3)  # Skip first 3 rows

# Method 2: Extract headers manually from row 3 (index 2)
df_raw = pd.read_excel('file.xlsx')
column_names = df_raw.iloc[2].tolist()  # Get row 3 as headers
df = pd.read_excel('file.xlsx', skiprows=3)
df.columns = column_names
```

**Key Columns**:
- `EstablishmentNumber`: Primary key for joining datasets (format: P####, M####, combinations)
- `EstablishmentName`: Facility name
- `InspectionDate`: Date of inspection
- `NonComplianceId`: Formal violations (very rare)
- `MOINumber`: Memorandum of Interview (welfare concerns)
- `NRNumber`: Noncompliance Record number
- `MOIDescription`: Detailed incident descriptions

---

### 2. USDA FSIS JSON Files (Laboratory Sampling Data)

**Format**: `.json` files with deeply nested structures

**Common Structure**:
```json
[
  {
    "metadata": {...},
    "data": {
      "primary_table_data": [...],      // Main sample records
      "secondary_table_data": [...]     // Detailed pathogen characterization
    },
    "appendix": {...}
  }
]
```

**Obstacle**: Data is nested inside a list containing a dict, not directly readable by `pd.DataFrame()`.

**Solution**:
```python
import json
import pandas as pd

# Load JSON
with open('file.json', 'r') as f:
    json_data = json.load(f)

# Extract from nested structure
if isinstance(json_data, list):
    data_dict = json_data[0]  # First item in list
    df = pd.DataFrame(data_dict['data']['primary_table_data'])
else:
    df = pd.DataFrame(json_data)

# Always verify structure first
print("Keys:", list(data_dict.keys()))
print("Data keys:", list(data_dict['data'].keys()))
```

**Key Columns in primary_table_data**:
- `establishment_number`: Join key (matches GCP EstablishmentNumber)
- `establishment_name`: Facility name
- `collection_date`: Sample collection date
- `sample_source_name`: Product type
- `salmonella_sp_analysis`: Result (Positive/Negative)
- `campylobacter_analysis_1ml`: Result (Positive/Negative)

---

### 3. USDA Consumption Data (CSV)

**Format**: `.csv` files, typically well-structured

**Common Structure**: Time series with demographic breakdowns

**Key Columns**:
- `food_group`: Category (e.g., "Protein foods, cured meat")
- `food_source`: FAH (Food at Home) or FAFH (Food Away From Home)
- Survey year columns with mean/SE values

**Obstacle**: Wide format with years as columns

**Solution**:
```python
# Read CSV
df = pd.read_csv('file.csv')

# Melt to long format if needed
df_long = pd.melt(df,
                  id_vars=['food_group', 'food_source'],
                  var_name='year',
                  value_name='consumption')
```

---

## Python Environment Issues

### Common Problem: pandas Not Found

**Root Cause**: Project uses pyenv with Python 3.6.15, but pandas may not be installed in that environment.

**Workaround**: Use system Python that already has pandas:
```bash
/opt/salt/bin/python3.7 script.py
```

**If Installing pandas**:
```bash
# Takes a long time (building numpy from source on older Python)
python3 -m pip install --user pandas openpyxl

# May see warnings about lzma module - safe to ignore
```

**Best Practice**:
1. Try system Python first: `/opt/salt/bin/python3.7`
2. If that fails, install in user environment (will take 5-10 minutes)
3. Always suppress lzma warnings: `warnings.filterwarnings('ignore')`

---

## Data Exploration Pattern

### Standard Exploration Script Template

```python
#!/usr/bin/env python3
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("DATA OVERVIEW")
print("=" * 80)

# 1. Load the data (adjust based on format)
# For Excel with headers:
df_raw = pd.read_excel('data/file.xlsx')
column_names = df_raw.iloc[2].tolist()
df = pd.read_excel('data/file.xlsx', skiprows=3)
df.columns = column_names

# For JSON:
# with open('data/file.json', 'r') as f:
#     json_data = json.load(f)
# df = pd.DataFrame(json_data[0]['data']['primary_table_data'])

# 2. Basic stats
print(f"Total records: {len(df):,}")
print(f"Unique establishments: {df['establishment_column'].nunique()}")

# 3. Column discovery
print("\nColumns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# 4. Sample data
print("\nSample data:")
print(df.head(3))

# 5. Search for specific patterns (if needed)
# Example: Find establishments by number
establishment_num = "P2186"
matches = df[df['EstablishmentNumber'].astype(str).str.contains(establishment_num, na=False)]
print(f"\nFound {len(matches)} records for {establishment_num}")

# 6. Keyword search across all columns
keywords = ['keyword1', 'keyword2']
for keyword in keywords:
    for col in df.columns:
        if df[col].astype(str).str.contains(keyword, case=False, na=False).any():
            matches = df[df[col].astype(str).str.contains(keyword, case=False, na=False)]
            print(f"Keyword '{keyword}' found in {col}: {len(matches)} matches")

print("=" * 80)
```

---

## Common Analysis Tasks

### 1. Aggregate Data by Establishment

**Use Case**: Summarize inspection or sampling activity per facility

```python
# Aggregate GCP inspections by establishment
gcp_summary = df.groupby(['EstablishmentNumber', 'EstablishmentName']).agg({
    'InspectionDate': 'count',                    # Total inspections
    'NonComplianceId': lambda x: x.notna().sum(), # Count NRs
    'MOINumber': lambda x: x.notna().sum()        # Count MOIs
}).reset_index()

gcp_summary.columns = ['EstablishmentNumber', 'EstablishmentName',
                       'TotalInspections', 'TotalNRs', 'TotalMOIs']
```

### 2. Count Positive Pathogen Results

```python
# Aggregate lab results by establishment
lab_summary = df.groupby('establishment_number').agg({
    'form_id': 'count',  # Total samples
    'salmonella_sp_analysis': lambda x: (x == 'Positive').sum(),
    'campylobacter_analysis_1ml': lambda x: (x == 'Positive').sum()
}).reset_index()

lab_summary.columns = ['EstablishmentNumber', 'TotalSamples',
                       'SalmonellaPositive', 'CampylobacterPositive']

# Calculate positive rates
lab_summary['SalmonellaRate'] = (
    lab_summary['SalmonellaPositive'] / lab_summary['TotalSamples'] * 100
).round(2)
```

### 3. Join Datasets by Establishment

**Key**: Use `EstablishmentNumber` as the join key

```python
# Full outer join to preserve all establishments
merged = gcp_summary.merge(
    lab_summary,
    on='EstablishmentNumber',
    how='outer',
    indicator=True  # Track which dataset each record came from
)

# Check join quality
print(f"In both datasets: {(merged['_merge'] == 'both').sum()}")
print(f"Only in GCP: {(merged['_merge'] == 'left_only').sum()}")
print(f"Only in Lab: {(merged['_merge'] == 'right_only').sum()}")

# Analyze subset with both datasets
both = merged[merged['_merge'] == 'both']
```

### 4. Time Series Analysis

```python
# Convert dates
df['collection_date'] = pd.to_datetime(df['collection_date'])
df['year_month'] = df['collection_date'].dt.to_period('M')

# Group by month
monthly = df.groupby('year_month').agg({
    'form_id': 'count',
    'salmonella_sp_analysis': lambda x: (x == 'Positive').sum()
}).reset_index()

monthly.columns = ['Month', 'Samples', 'Positives']
monthly['PositiveRate'] = (monthly['Positives'] / monthly['Samples'] * 100).round(2)
```

### 5. Find Top/Bottom Performers

```python
# Top establishments by inspection count
top_inspected = gcp_summary.sort_values('TotalInspections', ascending=False).head(15)

# Establishments with most welfare concerns
top_moi = gcp_summary[gcp_summary['TotalMOIs'] > 0].sort_values('TotalMOIs', ascending=False)

# Establishments with highest pathogen rates
high_contamination = lab_summary[lab_summary['TotalSamples'] > 10].sort_values('SalmonellaRate', ascending=False).head(15)
```

---

## Documentation Best Practices

### When to Create Analysis Documents

Create a new markdown document in `docs/` for:
1. **New dataset analysis**: First exploration of a dataset
2. **Cross-dataset joins**: Integration of multiple data sources
3. **Incident investigations**: Specific establishment or event analysis
4. **Hypothesis testing**: Research question with data evidence
5. **Methodology documentation**: Non-trivial analytical approaches

### Document Structure Template

```markdown
# [Title]: [Brief Description]

**Document Date**: [Date]
**Analysis Type**: [Exploratory/Comparative/Incident Investigation]

---

## Data Sources

### Primary Sources
- **File**: `data/filename.ext`
- **Description**: What the dataset contains
- **Period**: Time coverage
- **Records**: Record count
- **Key Fields**: Important columns

### Derived/Joined Datasets
- **Output File**: `data/output_filename.csv`
- **Linking Field**: Join key used
- **Join Type**: Inner/outer/left/right

---

## Overview

[Executive summary of findings]

---

## Analysis

[Detailed analysis sections]

---

## Key Findings

1. **Finding 1**: [Description with numbers]
2. **Finding 2**: [Description with numbers]

---

## Data Quality Notes

[Document any limitations, missing data, or caveats]

---

## Methodology

[Describe how analysis was performed, tools used]

**Analysis Script**: `script_name.py` (if applicable)

---

## References

- Primary data sources with full paths
- Related documentation
- Regulatory references

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial analysis |
```

### Naming Convention

Use sequential numbering for documents:
- `1-research.md` - Initial exploration
- `2-data-comparison-analysis.md` - Comparative analysis
- `8-gcp-fy2024-georges-foods-incident.md` - Specific incident
- `9-gcp-lab-joined-analysis.md` - Cross-dataset integration

---

## Common Analysis Patterns

### Pattern 1: "Popularity vs Contamination" Analysis

**Question**: Do popular foods have higher contamination rates?

**Required Data**:
1. Consumption data (USDA food intake surveys)
2. Lab sampling data (pathogen detection rates)
3. Product category mapping

**Challenges**:
- Consumption categories don't match lab categories exactly
- Time period mismatches (consumption data lags lab data)
- "Popularity" vs "consumption" vs "sales" distinctions

**Approach**:
```python
# 1. Extract relevant consumption data
consumption = df[df['food_group'].str.contains('cured meat|poultry|pork')]

# 2. Calculate contamination rates by product category
contamination = lab_df.groupby('sample_source_name').agg({
    'form_id': 'count',
    'salmonella_sp_analysis': lambda x: (x == 'Positive').sum()
})
contamination['rate'] = contamination['salmonella_sp_analysis'] / contamination['form_id']

# 3. Map categories (manual mapping required)
# Document mapping decisions in analysis doc

# 4. Correlate consumption with contamination
# Note: Document time period mismatch
```

### Pattern 2: "Establishment Risk Profile" Analysis

**Question**: Which establishments have multiple risk factors?

**Required Data**:
1. GCP inspection data (welfare violations)
2. Lab sampling data (pathogen detection)

**Approach**:
```python
# Join datasets by establishment
risk_profile = gcp_summary.merge(lab_summary, on='EstablishmentNumber', how='outer')

# Create risk indicators
risk_profile['HasMOIs'] = risk_profile['TotalMOIs'] > 0
risk_profile['HasNRs'] = risk_profile['TotalNRs'] > 0
risk_profile['HighPathogen'] = risk_profile['SalmonellaRate'] > 10.0

# Multi-factor risk
risk_profile['RiskFactors'] = (
    risk_profile['HasMOIs'].astype(int) +
    risk_profile['HasNRs'].astype(int) +
    risk_profile['HighPathogen'].astype(int)
)

# High-risk establishments (2+ factors)
high_risk = risk_profile[risk_profile['RiskFactors'] >= 2]
```

### Pattern 3: "Temporal Trend" Analysis

**Question**: Are contamination rates increasing or decreasing?

**Approach**:
```python
# By month/year
df['date'] = pd.to_datetime(df['collection_date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Calculate rate by time period
trends = df.groupby(['year', 'month']).agg({
    'form_id': 'count',
    'salmonella_sp_analysis': lambda x: (x == 'Positive').sum()
}).reset_index()

trends['rate'] = trends['salmonella_sp_analysis'] / trends['form_id'] * 100

# Seasonal patterns
seasonal = df.groupby('month').agg({
    'salmonella_sp_analysis': lambda x: (x == 'Positive').sum() / len(x) * 100
})
```

---

## Key Terminology

### FSIS Inspection Terms

- **GCP (Good Commercial Practices)**: Humane handling and slaughter practices for poultry
- **NR (Noncompliance Record)**: Formal violation requiring demonstrated loss of process control
- **MOI (Memorandum of Interview)**: Documentation of welfare concerns (not a formal violation)
- **IPP (Inspection Program Personnel)**: FSIS inspectors
- **Establishment Number**: Unique facility identifier (P#### for poultry, M#### for meat)

### Lab Sampling Terms

- **form_id**: Unique sample identifier (primary key)
- **sample_number**: Test identifier (multiple tests per form_id)
- **primary_table_data**: Main sample and test results
- **secondary_table_data**: Detailed pathogen characterization (serotypes, resistance)
- **RTE**: Ready-to-Eat products

### Pathogen Detection

- **Salmonella sp.**: Salmonella species detection
- **Campylobacter**: Common poultry pathogen
- **Listeria monocytogenes**: RTE product concern
- **MPN (Most Probable Number)**: Quantification method
- **CFU (Colony Forming Units)**: Bacterial count

---

## Critical Context: NRs vs MOIs

**Key Distinction**: Not all animal welfare issues result in formal violations.

**NR (Formal Violation)**:
- Requires demonstrated **loss of process control**
- Requires **ongoing pattern or trend**
- Example: Repeated birds entering scalder alive
- Very rare: Only 5 NRs in 105,814 GCP inspections (0.005%)

**MOI (Documented Concern)**:
- **Isolated incidents** of mistreatment
- Does NOT indicate loss of process control
- Documents discussion with establishment
- More common: 174 MOIs in FY2024 (0.16%)
- Establishment can object to MOI content

**Analysis Implication**:
- Don't treat MOIs as equivalent to violations
- MOI count indicates proactive oversight, not necessarily poor performance
- 35x more MOIs than NRs reflects this threshold difference

**Reference**: See `docs/8-gcp-fy2024-georges-foods-incident.md` for detailed NR vs MOI framework based on FSIS Directive 6110.1

---

## Troubleshooting Guide

### Issue: "Column not found" KeyError

**Cause**: Excel headers weren't parsed correctly or JSON structure unexpected

**Solution**:
```python
# Always inspect structure first
print("Columns:", df.columns.tolist())
print("First row:", df.iloc[0])

# For Excel, verify header row
df_raw = pd.read_excel('file.xlsx')
print("Row 2:", df_raw.iloc[2].tolist())
```

### Issue: Empty results when filtering

**Cause**: Data type mismatch (e.g., searching string in numeric column)

**Solution**:
```python
# Convert to string for pattern matching
df[df['column'].astype(str).str.contains('pattern', na=False)]

# Check data types
print(df.dtypes)
```

### Issue: Join produces no matches

**Cause**: Establishment number format differences

**Solution**:
```python
# Standardize format
df1['EstablishmentNumber'] = df1['EstablishmentNumber'].astype(str).str.strip()
df2['establishment_number'] = df2['establishment_number'].astype(str).str.strip()

# Check for common values
common = set(df1['EstablishmentNumber']) & set(df2['establishment_number'])
print(f"Common establishments: {len(common)}")
```

### Issue: Memory error loading large JSON

**Cause**: JSON file is very large (100MB+)

**Solution**:
```python
# Read in chunks or extract only needed fields
import ijson

with open('file.json', 'rb') as f:
    objects = ijson.items(f, 'item.data.primary_table_data.item')
    data = []
    for obj in objects:
        # Process incrementally
        data.append(obj)
        if len(data) >= 10000:  # Process in batches
            break
```

---

## When to Write Python Scripts

### Use Python Scripts When:

1. **Exploratory analysis**: Don't know data structure yet
2. **Complex data wrangling**: Nested JSON, header issues
3. **Iterative searches**: Finding specific records/patterns
4. **Reproducible analysis**: Need to re-run same analysis

### Script Best Practices:

```python
#!/usr/bin/env python3
"""
Brief description of what this script does
"""

import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 80)
    print("SCRIPT TITLE")
    print("=" * 80)

    # Load data
    print("\nLoading data...")
    df = load_data()

    # Analysis steps
    print("\nAnalyzing...")
    results = analyze(df)

    # Output
    print("\nSaving results...")
    results.to_csv('output.csv', index=False)
    print("✅ Done!")

def load_data():
    """Load and clean data"""
    # Implementation
    pass

def analyze(df):
    """Perform analysis"""
    # Implementation
    pass

if __name__ == '__main__':
    main()
```

### Save Scripts To:
- Root directory: `analyze_gcp_data.py`, `join_datasets.py`
- Name descriptively based on function
- Don't commit to git unless part of workflow

---

## Output Files Best Practices

### Save Analysis Results As:

1. **CSV for joined/aggregated data**: `data/joined_gcp_lab_poultry_data.csv`
2. **Markdown for analysis reports**: `docs/9-gcp-lab-joined-analysis.md`
3. **JSON for structured metadata**: Only if needed for further processing

### Always Document:
- Input files used
- Processing steps
- Output file location
- Date generated
- Any filters or exclusions applied

---

## Quick Reference Commands

```bash
# Check Python environment
which python3
python3 --version

# List data files
ls -lh data/

# Run analysis script with system Python
/opt/salt/bin/python3.7 script.py

# Check pandas installation
python3 -c "import pandas; print(pandas.__version__)"

# Install required packages
python3 -m pip install --user pandas openpyxl
```

---

## Related Documentation

- **GCP Incident Analysis**: `docs/8-gcp-fy2024-georges-foods-incident.md`
- **Joined Dataset Analysis**: `docs/9-gcp-lab-joined-analysis.md`
- **Consumption Analysis**: `docs/4-consumption-data-analysis.md`
- **Pork Sausage Analysis**: `docs/5-pork-sausage-analysis.md`

---

## Skill Maintenance

This skill should be updated when:
- New data formats are encountered
- New analysis patterns emerge
- Obstacles and solutions are discovered
- User research interests evolve

**Last Major Update**: March 2, 2026 - Initial skill creation based on GCP and lab sampling analysis
