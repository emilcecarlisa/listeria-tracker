# Data Directory

This directory contains USDA FSIS datasets used for food safety analysis.

## Files in Repository

These smaller files are tracked in git:
- `gcpArchiveFy2024.xlsx` - Good Commercial Practices inspection data (FY2024)
- `establishmentCategories202601.csv` - FSIS establishment categories
- `samplingProjectResults.csv` - Sampling project results
- `joinedGcpLabPoultryData.csv` - Joined GCP and lab sampling data (derived)
- `usFoodGroupIntakesBySource.csv` - USDA consumption data
- `fsisRecallSummary2025.xlsx` - FSIS recall summary data (2025)

## Large Files (Not in Repository)

These files exceed GitHub's 100MB limit and must be downloaded separately:

### Laboratory Sampling Data (FY2025)

**Files needed:**
- `labSamplingRawPorkFy2025.json` - Raw pork product sampling (4.8 MB)
- `labSamplingRawPoultryFy2025.json` - Raw poultry product sampling (102 MB)
- `labSamplingRteFy2025.json` - Ready-to-eat product sampling (47 MB)

**Where to download:**
- Source: USDA FSIS Data Discovery Portal
- URL: https://www.fsis.usda.gov/science-data/data-sets-visualizations

**How to download:**
1. Visit the FSIS Data Discovery Portal
2. Navigate to "Laboratory Sampling Data"
3. Download the FY2025 datasets for:
   - Raw Pork Product Sampling
   - Raw Poultry Product Sampling
   - Ready-to-Eat (RTE) Product Sampling
4. Place the JSON files in this `data/` directory

## Analysis Outputs

Generated files from analysis scripts:
- `joinedGcpLabPoultryData.csv` - Merged establishment-level data from GCP inspections and lab sampling

See `docs/` directory for detailed analysis documentation.
