# Joined Analysis: GCP Inspections & Laboratory Sampling Data

**Document Date**: March 2, 2026
**Analysis Type**: Cross-dataset integration of poultry handling practices and pathogen detection

---

## Data Sources

### Primary Source Datasets

1. **GCP Poultry Handling Data (FY2024)**
   - File: `data/gcpArchiveFy2024.xlsx`
   - Description: Poultry Good Commercial Practices inspection records
   - Period: October 1, 2023 - September 30, 2024
   - Records: 105,814 inspections
   - Establishments: 331 unique facilities

2. **Raw Poultry Laboratory Sampling Data (FY2025)**
   - File: `data/labSamplingRawPoultryFy2025.json`
   - Description: Laboratory testing for Salmonella and Campylobacter in raw poultry
   - Period: Fiscal Year 2025
   - Records: 28,564 samples
   - Establishments: 786 unique facilities

### Joined Dataset

**Output File**: `data/joinedGcpLabPoultryData.csv`

**Linking Field**: `EstablishmentNumber` (format: P####, M####, or combinations)

**Join Type**: Full outer join (includes establishments from either or both datasets)

---

## Dataset Coverage

| Category | Count | Percentage |
|----------|-------|------------|
| **Total Unique Establishments** | 865 | 100% |
| Establishments in BOTH datasets | 252 | 29.1% |
| Only in GCP data (no lab sampling) | 79 | 9.1% |
| Only in Lab data (no GCP inspections) | 534 | 61.7% |

**Key Observation**: Only 29.1% of establishments appear in both datasets, indicating that GCP inspections and lab sampling programs target somewhat different facility populations.

---

## Joined Dataset Schema

### GCP Inspection Metrics (FY2024)
- `EstablishmentNumber`: USDA establishment identifier
- `EstablishmentName`: Facility name
- `EstablishmentID`: Internal FSIS ID
- `GCP_TotalInspections`: Count of GCP inspection tasks performed
- `GCP_TotalNRs`: Count of formal Noncompliance Records (violations)
- `GCP_TotalMOIs`: Count of Memorandums of Interview (welfare concerns)

### Laboratory Sampling Metrics (FY2025)
- `Lab_TotalSamples`: Count of laboratory samples collected
- `Lab_SalmonellaPositive`: Count of Salmonella-positive results
- `Lab_CampylobacterPositive`: Count of Campylobacter-positive results
- `Lab_SalmonellaPositiveRate`: Percentage of samples testing positive for Salmonella
- `Lab_CampylobacterPositiveRate`: Percentage of samples testing positive for Campylobacter

### Join Metadata
- `_merge`: Indicator showing data source(s) for each record
  - `both`: In both GCP and Lab datasets
  - `left_only`: Only in GCP dataset
  - `right_only`: Only in Lab dataset

---

## Analysis: Establishments with Both GCP and Lab Data

**Subset**: 252 establishments with data from both inspection programs

### GCP Inspection Statistics (FY2024)

| Metric | Value |
|--------|-------|
| Total Inspections | 98,149 |
| Average Inspections per Establishment | 389.5 |
| Establishments with Formal Violations (NRs) | 3 (1.2%) |
| Establishments with Animal Welfare Concerns (MOIs) | 73 (29.0%) |
| Total MOIs Issued | 170 |

**Key Finding**: Nearly one-third (29%) of establishments with both datasets received at least one MOI for animal welfare concerns during FY2024.

### Laboratory Sampling Statistics (FY2025)

| Metric | Value |
|--------|-------|
| Total Samples | 18,869 |
| Average Samples per Establishment | 74.9 |
| Salmonella Positive Results | 1,470 |
| **Overall Salmonella Positive Rate** | **7.79%** |
| Campylobacter Positive Results | 0 |
| Establishments with Any Positive Result | 219 (86.9%) |

**Key Finding**: The Salmonella positive rate of 7.79% indicates ongoing contamination challenges in raw poultry. Note that Campylobacter testing showed zero positives, which may reflect testing methodology or data collection limitations.

---

## Top Findings

### Establishments with Highest Animal Welfare Concerns (MOIs)

| Rank | Establishment Number | Name | GCP Inspections | Total MOIs | Lab Samples | Salmonella Positive |
|------|---------------------|------|-----------------|------------|-------------|---------------------|
| 1 | P7487 | Koch Foods, LLC | 510 | 26 | 56 | 3 |
| 2 | M32130+P32130+V32130 | Dakota Provisions LLC | 410 | 14 | 21 | 1 |
| 3 | M4181+P4181 | Mao Foods, Inc. | 208 | 7 | 45 | 0 |
| 4 | P208+V208 | George's Processing, Inc. | 514 | 6 | 106 | 8 |
| 5 | P165H | Bachoco OK Foods | 455 | 6 | 103 | 5 |

**Analysis**: Koch Foods, LLC (P7487) had 26 MOIs—more than any other establishment—representing 15% of all MOIs among establishments with both datasets.

### Establishments with Highest Pathogen Detection

| Rank | Establishment Number | Name | Lab Samples | Salmonella Positive | Positive Rate | GCP MOIs |
|------|---------------------|------|-------------|---------------------|---------------|----------|
| 1 | P1243 | Perdue Foods, LLC | 173 | 43 | 24.9% | 2 |
| 2 | P39915+V39915 | Locust Point Farms, LLC | 72 | 38 | 52.8% | 0 |
| 3 | P2178 | Perdue Foods LLC | 170 | 37 | 21.8% | 0 |
| 4 | M27389+P27389+V27389 | Pitman Farms | 170 | 37 | 21.8% | 0 |
| 5 | P46897 | Ihsan Farms, LLC | 49 | 31 | 63.3% | 0 |

**Analysis**: Locust Point Farms (P39915+V39915) had the highest Salmonella positive rate at 52.8%, and Ihsan Farms (P46897) had an alarming 63.3% positive rate. Neither establishment had MOIs for animal welfare concerns.

### Most Intensively Inspected Establishments (with Lab Data)

| Establishment Number | Name | GCP Inspections | MOIs | Lab Samples | Salmonella Positive |
|---------------------|------|-----------------|------|-------------|---------------------|
| P622 | Tyson Foods, Inc. | 1,248 | 1 | 104 | 6 |
| M6137+P6137 | Foster Poultry Farms, LLC | 1,028 | 1 | 115 | 16 |
| P46374 | Sanderson Farms Processing Inc. | 964 | 0 | 105 | 4 |
| P6505 | Norman W. Fries, Inc. | 873 | 0 | 115 | 6 |
| P7927 | Amick Farms, LLC | 806 | 2 | 111 | 2 |

**Analysis**: Large, high-volume establishments receive significantly more GCP inspections. Tyson Foods (P622) had the most inspections at 1,248—nearly 12.7% of all inspections among establishments with both datasets.

---

## Key Observations

### 1. No Strong Correlation Between Welfare Violations and Pathogen Detection

Establishments with high numbers of animal welfare concerns (MOIs) do not necessarily have high pathogen positive rates, and vice versa:

- **Koch Foods (P7487)**: 26 MOIs but only 5.4% Salmonella positive rate
- **Locust Point Farms (P39915+V39915)**: 0 MOIs but 52.8% Salmonella positive rate
- **Ihsan Farms (P46897)**: 0 MOIs but 63.3% Salmonella positive rate

This suggests that animal welfare practices and food safety controls may be independent operational areas.

### 2. Time Period Mismatch

- GCP data: FY2024 (Oct 2023 - Sep 2024)
- Lab data: FY2025 (Oct 2024 - Sep 2025)

**Implication**: These datasets represent consecutive time periods, not the same period. Any correlations should be interpreted as lagged relationships, where FY2024 handling practices might influence FY2025 pathogen levels.

### 3. Large Establishments Dominate Both Programs

The top 15 most-inspected establishments (1.8% of facilities) account for:
- 11,437 inspections (11.7% of total inspections)
- Major brands: Tyson, Perdue, Pilgrim's Pride, Foster Farms, Sanderson Farms

### 4. High Salmonella Prevalence

The overall 7.79% Salmonella positive rate across 18,869 samples indicates:
- Salmonella remains a persistent challenge in raw poultry
- 219 out of 252 establishments (86.9%) had at least one positive sample
- Wide variation in positive rates (0% to 63.3%)

---

## Establishments of Note

### George's Foods, LLC (P2186)

**Reference**: See detailed incident report in `docs/gcpFy2024GeorgesFoodsIncident.md`

| Metric | Value |
|--------|-------|
| GCP Inspections | 500 |
| MOIs | 2 |
| Lab Samples | 118 |
| Salmonella Positive | 8 |
| Salmonella Positive Rate | 6.78% |

George's Foods had 2 MOIs including the documented April 12, 2024 chicken-throwing incident, and a Salmonella positive rate slightly below the overall average.

---

## Data Quality Notes

### Campylobacter Data
The lab dataset shows **zero Campylobacter positives** across all 28,564 samples, which is unusual given that Campylobacter is highly prevalent in poultry. Possible explanations:
- Testing was not performed for Campylobacter in this period
- Data was not included in the FY2025 dataset
- Testing methodology changed
- Results are in secondary table data not analyzed

### Establishment Number Variations
Some establishments have complex number formats (e.g., "M32130+P32130+V32130"), indicating:
- Multiple facility types at the same location (M=meat, P=poultry, V=voluntary)
- Different inspection categories
- These were treated as single establishments in this analysis

---

## Methodology

### Data Processing Steps

1. **GCP Data Aggregation**
   - Loaded raw inspection records from Excel (105,814 records)
   - Grouped by EstablishmentNumber, EstablishmentName, EstablishmentID
   - Counted: total inspections, NRs (formal violations), MOIs (welfare concerns)
   - Result: 331 unique establishments

2. **Lab Data Aggregation**
   - Loaded JSON structure with nested primary_table_data
   - Extracted 28,564 sample records
   - Counted Salmonella and Campylobacter positive results per establishment
   - Calculated positive rates
   - Result: 786 unique establishments

3. **Join Operation**
   - Full outer join on EstablishmentNumber
   - Preserved all establishments from either dataset
   - Added merge indicator for data source tracking
   - Result: 865 unique establishments

### Analysis Tools
- Python 3.7 with pandas library
- Data processing script: `analyze_gcp_data.py`

---

## Use Cases for Joined Dataset

### Research Applications
1. **Risk Assessment**: Identify establishments with both welfare and food safety concerns
2. **Predictive Modeling**: Test whether animal handling practices predict pathogen contamination
3. **Resource Allocation**: Target inspection resources based on combined risk factors
4. **Trend Analysis**: Track establishment performance across multiple dimensions
5. **Comparative Analysis**: Benchmark establishment performance against peers

### Regulatory Applications
1. **Enforcement Prioritization**: Focus on establishments with multiple concern areas
2. **Compliance Verification**: Cross-reference inspection and sampling outcomes
3. **Pattern Detection**: Identify systematic vs. isolated issues
4. **Intervention Effectiveness**: Evaluate whether MOIs lead to improved outcomes

---

## Limitations

1. **Time Lag**: GCP (FY2024) and Lab (FY2025) data are from consecutive, not concurrent periods

2. **Incomplete Coverage**: Only 29.1% of establishments appear in both datasets

3. **Sampling Bias**:
   - Lab sampling may target high-risk establishments
   - GCP inspections are more comprehensive across all slaughter facilities

4. **Campylobacter Data**: Appears incomplete or unavailable in this dataset

5. **Causality**: Cannot establish causal relationships between welfare practices and pathogen levels from observational data

6. **Reporting Lag**: Data extracted March 31, 2025 for lab data; may not reflect most recent conditions

---

## Related Documentation

- **GCP Incident Report**: `docs/gcpFy2024GeorgesFoodsIncident.md` - Detailed analysis of George's Foods April 2024 incident and NR vs MOI framework
- **FSIS Directive 6110.1**: Guidance on writing NRs and MOIs for poultry mistreatment
- **Regulation 9 CFR 381.65(b)**: Good Commercial Practices requirements for poultry slaughter

---

## Future Analysis Opportunities

1. **Temporal Analysis**: Once FY2025 GCP data becomes available, analyze concurrent time periods
2. **Establishment Characteristics**: Join with establishment categories dataset to analyze by facility type/size
3. **Geographic Patterns**: Analyze welfare and pathogen patterns by state
4. **Product Type Analysis**: Examine differences between chicken vs. turkey operations
5. **Intervention Studies**: Track establishments before/after MOIs to measure corrective action effectiveness
6. **Multi-year Trends**: Expand analysis as additional fiscal years become available

---

## References

### Data Sources
- `data/gcpArchiveFy2024.xlsx` - GCP Poultry Handling FY2024
- `data/labSamplingRawPoultryFy2025.json` - Lab Sampling FY2025
- `data/joinedGcpLabPoultryData.csv` - **Output: Joined dataset for analysis**

### Regulatory Framework
- USDA FSIS Data Transparency Initiative
- 9 CFR 381.65(b) - Good Commercial Practices
- FSIS Directive 6110.1 - NR and MOI Documentation

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-02 | 1.0 | Initial joined analysis of GCP FY2024 and Lab FY2025 data; documented join methodology, coverage analysis, and key findings |

