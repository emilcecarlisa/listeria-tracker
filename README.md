# Listeria Tracker: Pathogen Research in Meat Production

This project analyzes pathogen contamination in meat products, correlating dietary consumption patterns, laboratory sampling results, product recalls, and commercial practices data to understand food safety trends.

## Project Objective

Create an interactive dashboard that tells a story about how factory-produced meat shows increasing contamination rates, and how better animal welfare practices might reduce pathogen contamination.

## Data Source Mapping

| Dashboard Component | Data Source(s) | Analysis Documents | Status |
|---------------------|---------------|-------------------|---------|
| **Foods People Eat** | `usFoodGroupIntakesBySource.csv` | [`consumptionDataAnalysis.md`](docs/consumptionDataAnalysis.md) | ✓ Complete |
| **Foods Contaminated with Pathogens** | `joinedGcpLabPoultryData.csv`<br>`labSamplingRawPorkFy2025.json`<br>`labSamplingRawPoultryFy2025.json`<br>`labSamplingRteFy2025.json` | [`dataComparisonAnalysis.md`](docs/dataComparisonAnalysis.md)<br>[`porkSausageAnalysis.md`](docs/porkSausageAnalysis.md)<br>[`jupyterVisualizationPseudocode.md`](docs/jupyterVisualizationPseudocode.md)<br>[`porkVsChickenComparison.md`](docs/porkVsChickenComparison.md) | ✓ Complete |
| **What Foods Are Recalled Most?** | `fsisRecallSummary2025.xlsx` | *To be created* | 🔄 In Progress |
| **Commercial Practices & Violations** | `gcpArchiveFy2024.xlsx` | [`gcpFy2024GeorgesFoodsIncident.md`](docs/gcpFy2024GeorgesFoodsIncident.md)<br>[`gcpLabJoinedAnalysis.md`](docs/gcpLabJoinedAnalysis.md) | ✓ Complete |

## Data Files

### Files in Repository

Core analysis files tracked in git:
- `gcpArchiveFy2024.xlsx` - Good Commercial Practices inspection data (FY2024)
- `establishmentCategories202601.csv` - FSIS establishment categories
- `samplingProjectResults.csv` - Sampling project results
- `joinedGcpLabPoultryData.csv` - Joined GCP and lab sampling data (derived)
- `usFoodGroupIntakesBySource.csv` - USDA consumption data (1977-2018)
- `fsisRecallSummary2025.xlsx` - FSIS recall summary data (2025)

### Large Files (Not in Repository)

These files exceed GitHub's 100MB limit and must be downloaded separately:

**Laboratory Sampling Data (FY2025)**

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
4. Place the JSON files in the `data/` directory

## Analysis Outputs

Generated files from analysis scripts:
- `joinedGcpLabPoultryData.csv` - Merged establishment-level data from GCP inspections and lab sampling

## Documentation Structure

### Analysis Documents (`docs/`)
- `consumptionDataAnalysis.md` - US food consumption patterns (plant vs. animal)
- `dataComparisonAnalysis.md` - Cross-dataset comparison of lab and GCP data
- `porkSausageAnalysis.md` - Pork sausage contamination analysis
- `porkVsChickenComparison.md` - Comparative analysis of pork and chicken contamination
- `gcpFy2024GeorgesFoodsIncident.md` - Case study of GCP violations
- `gcpLabJoinedAnalysis.md` - Joined GCP and laboratory data analysis
- `jupyterVisualizationPseudocode.md` - Visualization planning and pseudocode

### Visualizations (`visualizations/`)
- `consumptionTrends.ipynb` - Food consumption trends over time
- `consumptionVsContamination.ipynb` - Correlation analysis
- `productAnalysis.ipynb` - Product-level contamination analysis
- `programEffectiveness.ipynb` - FSIS program effectiveness metrics
- `stateMapChoropleth.ipynb` - Geographic distribution of contamination

### Scripts (`scripts/`)
- `analyzeGcpData.py` - GCP inspection data analysis

### Skills (`skills/`)
- `dataAnalysisSkill.md` - Comprehensive guide for USDA FSIS data analysis

## Key Findings & Data Gaps

### Completed Analysis
- ✓ Consumption patterns: Animal-based foods represent ~18.5% of total food intake
- ✓ Pathogen detection rates vary by product type (0.25-1.81% for poultry, 0.67-0.84% for pork)
- ✓ GCP violations are rare (0.005% NRs, 0.16% MOIs in FY2024)
- ✓ Establishment-level correlation between welfare practices and contamination

### Data Gaps Identified
- ⚠️ **Missing plant-based pathogen data**: No laboratory sampling data exists for plant-based products (vegetables, fruits, grains), making it difficult to compare animal vs. plant contamination rates fairly
- ⚠️ **RTE consumption granularity**: Consumption data doesn't separate ready-to-eat from raw products for most categories
- ⚠️ **Time period misalignment**: Consumption data (2017-2018) vs. Lab sampling data (FY2025)

## Next Steps

1. **Complete Recall Analysis** - Analyze `fsisRecallSummary2025.xlsx` to determine animal vs. plant recall rates
2. **Create Comprehensive Dashboard** - Consolidate all visualizations into a single interactive notebook
3. **Document Missing Data** - Formally document plant-based contamination data gap
4. **Develop Rating System** - Create establishment/brand rating system based on contamination and commercial practices

## Project Implementation Guide

See [`pathogenResearchInMeatProduction.md`](docs/pathogenResearchInMeatProduction.md) for detailed implementation plan and objectives.

## Skills and Tools

- Python 3.6+, pandas, openpyxl for data analysis
- Jupyter notebooks for visualization
- USDA FSIS data formats (Excel with metadata headers, nested JSON)

For detailed guidance on analyzing USDA FSIS data, see [`dataAnalysisSkill.md`](skills/dataAnalysisSkill.md).
