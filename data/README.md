# Data Directory

This directory contains USDA FSIS datasets used for food safety analysis.

## Files in Repository

These smaller files are tracked in git:
- `0post-GCP_arch24.xlsx` - Good Commercial Practices inspection data (FY2024)
- `Dataset_EstablishmentCategories_202601.csv` - FSIS establishment categories
- `Dataset_QSR_SamplingProjectResultsData.csv` - Sampling project results
- `joined_gcp_lab_poultry_data.csv` - Joined GCP and lab sampling data (derived)
- `table-5-US-food-group-intakes-by-food-source.csv` - USDA consumption data

## Large Files (Not in Repository)

These files exceed GitHub's 100MB limit and must be downloaded separately:

### Laboratory Sampling Data (FY2025)

**Files needed:**
- `usda_fsis_data_product_establishment_specific_laboratory_sampling_raw_pork_product_fy2025.json` (4.8 MB)
- `usda_fsis_data_product_establishment_specific_laboratory_sampling_raw_poultry_product_fy2025.json` (102 MB)
- `usda_fsis_data_product_establishment_specific_laboratory_sampling_rte_product_fy2025.json` (47 MB)

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
- `joined_gcp_lab_poultry_data.csv` - Merged establishment-level data from GCP inspections and lab sampling

See `docs/` directory for detailed analysis documentation.
