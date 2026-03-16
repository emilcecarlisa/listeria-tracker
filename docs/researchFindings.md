# Listeria Tracker - Research Findings & Dashboard Proposal

## Executive Summary

This analysis examines USDA FSIS Ready-to-Eat (RTE) Product Sampling data for FY2025, focusing on Listeria monocytogenes and other pathogen detection in food processing establishments across the United States.

**Dataset Overview:**
- **Primary Dataset:** 27,211 sampling records
- **Secondary Dataset:** 443 detailed pathogen characterization records
- **Time Period:** October 1, 2024 - September 30, 2025 (FY2025)
- **Geographic Coverage:** All 50 states + 3 territories
- **Unique Establishments:** 2,364 food processing facilities

---

## Phase 1: Data Analysis Results

### Dataset Structure

#### Primary Dataset (27,211 records)
Contains sample collection information and initial test results with 28 columns:

**Key Identifiers:**
- `form_id` - Unique sample identifier
- `sample_number` - Test number within sample
- `establishment_id` - Facility identifier
- `establishment_number` - Official USDA establishment number
- `establishment_name` - Facility name

**Geographic & Temporal:**
- `establishment_state` - State/territory code (53 unique locations)
- `collection_date` - Sample collection date (YYYY-MM-DD format)

**Project Information:**
- `project_code` - Sampling program type (29 different programs)
- `project_name` - Human-readable program name

**Sample Characteristics:**
- `sample_source_name` - Type of sample (110 unique types)
- `production_alternative` - Production method/alternative

**Test Results:**
- `lm_listeria_analysis` - Listeria monocytogenes test result (Positive/Negative)
- `salmonella_sp_analysis` - Salmonella test result (Positive/Negative)
- `non_lm_listeria_analysis` - Non-Lm Listeria species test

#### Secondary Dataset (443 records)
Contains detailed characterization for positive pathogen samples with 99 columns:

**Genetic Characterization:**
- Allele codes (genetic fingerprints)
- Multi-locus sequence types (MLST)
- Whole genome sequencing data
- PFGE patterns (older typing method)

**Antibiotic Resistance:**
- 17 different antibiotics tested for Salmonella
- Resistance genotype and phenotype data

**Virulence & Stress Genes:**
- Resistance genotypes
- Stress genotypes
- Virulence genotypes

### Data Quality Assessment

#### Missing Data Analysis

**Completely Empty Columns (100% NULL):**
These columns exist but contain no data in FY2025:
- All Salmonella MPN (Most Probable Number) quantification fields
- All Listeria MPN quantification fields
- Test cancellation tracking fields

**Partially Missing Data:**
- `salmonella_sp_analysis`: 55.9% missing (many samples only tested for Listeria)
- `non_lm_listeria_analysis`: 28.3% missing (relatively new testing addition)
- `production_alternative`: 5.7% missing
- `lm_listeria_analysis`: 0.3% missing (nearly complete)

**Data Type Characteristics:**
- Dates: Properly formatted as YYYY-MM-DD
- IDs: Integer values (establishment_id, sample_number)
- Categorical: String values for test results, states, project codes
- Many fields stored as strings that could be converted to categorical types

---

## Key Findings

### 1. Pathogen Detection Rates

**Listeria monocytogenes:**
- Tested: 27,124 samples
- Positive: 208 samples
- **Detection Rate: 0.77%**

**Salmonella:**
- Tested: 11,995 samples
- Positive: 6 samples
- **Detection Rate: 0.05%**

**Interpretation:** Low positive rates indicate generally good food safety controls, but 208 Listeria positives warrant detailed tracking and investigation.

### 2. Geographic Distribution

**Top 10 States by Sample Volume:**
1. California: 2,829 samples (10.4%)
2. Texas: 2,225 samples (8.2%)
3. Illinois: 2,125 samples (7.8%)
4. Pennsylvania: 1,297 samples (4.8%)
5. New York: 1,071 samples (3.9%)
6. Georgia: 1,033 samples (3.8%)
7. New Jersey: 1,025 samples (3.8%)
8. Oklahoma: 882 samples (3.2%)
9. Ohio: 851 samples (3.1%)
10. Wisconsin: 791 samples (2.9%)

**Coverage:** All 50 states plus DC, Puerto Rico, and Guam

### 3. Sampling Programs

**Primary Project Types:**
1. **RTEPROD** (7,989 samples): General RTE product sampling
2. **RTEPROD_RISK** (2,699 samples): Risk-based RTE sampling
3. **RLMCONT_MWL** (2,499 samples): Risk-based food contact surface - Midwest Lab
4. **INTCONT_LM_E** (2,059 samples): Intensified (for-cause) contact surface - Eastern Lab
5. **RLMCONT_EL** (1,939 samples): Risk-based contact surface - Eastern Lab

**Program Categories:**
- **Routine/Random:** Regular surveillance sampling
- **Risk-Based:** Algorithm-driven targeted sampling
- **Intensified (IVT):** For-cause testing after positive results

### 4. Sample Types

**Most Common Sample Sources:**
1. Product Contact Surface Sponges: 10,135 (37.2%)
2. Non-Product Contact Surface Sponges: 2,600 (9.6%)
3. RTE Chicken Products: 1,208 (4.4%)
4. RTE Pork Products: 1,122 (4.1%)
5. RTE Pork Sausages: 952 (3.5%)

**Key Insight:** Environmental swabs (contact/non-contact surfaces) make up 47% of samples, indicating focus on facility contamination prevention.

### 5. Pathogen Characterization Insights

**Listeria monocytogenes Genetic Diversity:**
- 97 unique allele codes (genetic fingerprints)
- 201 total characterizations in secondary data

**Top Sequence Types (genetic lineages):**
1. ST9: 38 isolates (18.9%)
2. ST321: 37 isolates (18.4%)
3. ST5: 34 isolates (16.9%)
4. ST31: 10 isolates (5.0%)

**Significance:** Multiple sequence types indicate diverse contamination sources rather than a single outbreak strain.

**Salmonella Serotypes Detected:**
- 6 different serotypes in 6 positive samples
- Most notable: Infantis, Montevideo, Enteritidis, Johannesburg

---

## Phase 2: Dashboard Proposal

### Recommended Dashboard Components

Based on the data structure and public health priorities, I propose a multi-view dashboard focused on tracking, analyzing, and preventing Listeria and pathogen contamination in RTE food facilities.

---

### Dashboard View 1: **Geographic Outbreak Tracker**

**Purpose:** Visualize pathogen detection across the United States to identify geographic hotspots and regional patterns.

**Visualizations:**

1. **Interactive US Choropleth Map**
   - Color-coded states by:
     - Total samples collected
     - Positive detection rate (%)
     - Number of facilities tested
   - Click state for drill-down to facility-level data

2. **State-Level Bar Charts**
   - Top 10 states by positive detections
   - Positive rate comparison across states
   - Sample volume vs detection rate scatter plot

**Key Metrics Displayed:**
- Total positives by state
- Detection rate by state
- Facilities with repeated positives
- High-risk regions

**Data Required:**
- `establishment_state`
- `lm_listeria_analysis` / `salmonella_sp_analysis`
- `establishment_id` (for facility counting)

**Conclusions We Can Draw:**
- ✅ Identify geographic clusters of contamination
- ✅ Compare state-level food safety performance
- ✅ Identify states needing increased oversight
- ❌ Cannot determine specific outbreak locations without address-level data
- ❌ Cannot correlate with population density without external data

---

### Dashboard View 2: **Temporal Trend Analysis**

**Purpose:** Track pathogen detection over time to identify seasonal patterns, improvement trends, or emerging problems.

**Visualizations:**

1. **Time Series Line Chart**
   - Daily/weekly/monthly positive detection rate
   - Separate lines for Listeria vs Salmonella
   - Moving average trendlines
   - Annotations for significant events

2. **Calendar Heatmap**
   - Daily view showing positive/negative samples
   - Color intensity = sample volume
   - Quick visual identification of problem periods

3. **Seasonal Analysis**
   - Detection rates by month
   - Testing volume by month
   - Identify seasonal contamination patterns

**Key Metrics Displayed:**
- Rolling 7-day/30-day positive rate
- Year-over-year comparison (when multi-year data available)
- Days since last positive detection
- Testing velocity (samples per day)

**Data Required:**
- `collection_date`
- `lm_listeria_analysis` / `salmonella_sp_analysis`

**Conclusions We Can Draw:**
- ✅ Identify seasonal contamination patterns
- ✅ Track improvement over time
- ✅ Detect emerging outbreak signals
- ✅ Evaluate sampling program effectiveness
- ⚠️ Limited to one fiscal year currently (need historical data for better trends)

---

### Dashboard View 3: **Facility & Establishment Risk Profile**

**Purpose:** Identify high-risk facilities requiring increased attention and track establishment-level compliance.

**Visualizations:**

1. **Facility Risk Scorecard**
   - Table of facilities sorted by:
     - Number of positive samples
     - Positive detection rate
     - Days since last test
     - Days since last positive
   - Flag facilities with repeat positives
   - Color-coded risk levels (green/yellow/red)

2. **Establishment Detail View**
   - Single facility drill-down
   - Timeline of all samples
   - Product types produced
   - Sample source breakdown (product vs environment)
   - Genetic fingerprints of detected pathogens

3. **Repeat Offender Analysis**
   - Facilities with multiple positives
   - Time between positive detections
   - Whether same or different genetic strains

**Key Metrics Displayed:**
- Facilities with 2+ positives
- Average time between facility tests
- Establishments in intensified testing programs
- Geographic clustering of problem facilities

**Data Required:**
- `establishment_id`, `establishment_name`, `establishment_state`
- `lm_listeria_analysis` / `salmonella_sp_analysis`
- `collection_date`
- `project_code` (to identify IVT/for-cause testing)
- Secondary data: `lm_listeria_allele_code`, `lm_listeria_multi_locus_sequence`

**Conclusions We Can Draw:**
- ✅ Identify persistent contamination problems at specific facilities
- ✅ Determine if facility positives are related (same genetic strain)
- ✅ Track effectiveness of corrective actions
- ✅ Prioritize inspection resources
- ❌ Cannot determine root causes without additional investigation data

---

### Dashboard View 4: **Product & Sample Source Analysis**

**Purpose:** Identify which product types and sample locations are most associated with contamination.

**Visualizations:**

1. **Product Category Breakdown**
   - Bar chart of positive rates by product type
   - Top 10 product categories by sample volume
   - Top 10 product categories by positive rate
   - Tree map showing relative product sampling volumes

2. **Sample Source Heatmap**
   - Matrix showing:
     - Rows: Sample source type (Product/Contact Surface/Non-Contact)
     - Columns: Pathogen detected
     - Values: Positive rates or counts

3. **Environmental vs Product Contamination**
   - Comparison of positive rates:
     - Product samples
     - Food contact surfaces
     - Non-food contact surfaces
   - Connection analysis: Do environmental positives predict product positives?

**Key Metrics Displayed:**
- Highest-risk product categories
- Environmental contamination rate
- Product contamination rate
- Ratio of environmental to product positives

**Data Required:**
- `sample_source_name`
- `lm_listeria_analysis` / `salmonella_sp_analysis`
- Derived field: Sample type category (Product/Contact/Non-Contact)

**Conclusions We Can Draw:**
- ✅ Identify high-risk product categories (e.g., deli meats, sausages)
- ✅ Determine if contamination is environmental or product-level
- ✅ Evaluate effectiveness of environmental sampling programs
- ✅ Guide product-specific interventions
- ⚠️ Cannot determine causation (e.g., specific foods causing outbreaks) without epidemiological data

---

### Dashboard View 5: **Genetic Fingerprint & Outbreak Detection**

**Purpose:** Use whole genome sequencing data to identify potential outbreak clusters and track pathogen persistence.

**Visualizations:**

1. **Allele Code Network Diagram**
   - Nodes = Facilities
   - Edges = Shared allele codes (genetic matches)
   - Color = Sequence type (ST)
   - Size = Number of positives
   - Identify potential cross-contamination networks

2. **Sequence Type Distribution**
   - Bar chart of most common Listeria STs
   - Pie chart showing genetic diversity
   - Map overlay: Geographic distribution of specific STs

3. **Potential Outbreak Clusters**
   - Algorithm to identify:
     - Same allele code
     - Multiple facilities
     - Similar time period
   - Flag for investigation

4. **Virulence & Resistance Profile**
   - Bar charts showing prevalence of:
     - Antibiotic resistance genes
     - Virulence factors
     - Stress survival genes
   - Public health risk assessment

**Key Metrics Displayed:**
- Number of unique genetic strains
- Facilities sharing genetic strains
- High-risk genetic lineages
- Antibiotic resistance prevalence

**Data Required:**
- Secondary data: `lm_listeria_allele_code`, `lm_listeria_multi_locus_sequence`
- `lm_listeria_resistance_genotype`, `lm_listeria_virulence_genotype`
- `establishment_id`, `collection_date`

**Conclusions We Can Draw:**
- ✅ Identify potential outbreak clusters (same strain, multiple facilities)
- ✅ Track persistent strains within facilities
- ✅ Detect geographic spread of specific strains
- ✅ Assess public health risk based on virulence/resistance
- ⚠️ Cannot confirm outbreak without clinical case data
- ⚠️ Cannot determine transmission routes without supply chain data

---

### Dashboard View 6: **Sampling Program Effectiveness**

**Purpose:** Evaluate the performance of different USDA sampling programs and optimize resource allocation.

**Visualizations:**

1. **Program Comparison Table**
   - Rows: Project codes (RTEPROD, RTEPROD_RISK, IVT programs, etc.)
   - Columns: Samples collected, Positives found, Detection rate, Cost-effectiveness

2. **Risk-Based vs Random Sampling**
   - Side-by-side comparison of detection rates
   - Evaluation: Is risk-based sampling more effective?

3. **Intensified Testing Impact**
   - Before/after analysis for facilities entering IVT
   - Track positive rate trends after interventions

4. **Lab Performance**
   - Compare Eastern, Midwest, and Western lab results
   - Testing volume and turnaround time

**Key Metrics Displayed:**
- Detection rate by program type
- Samples per positive detection (efficiency)
- IVT program success rate
- Lab capacity utilization

**Data Required:**
- `project_code`, `project_name`
- `lm_listeria_analysis` / `salmonella_sp_analysis`
- `collection_date`

**Conclusions We Can Draw:**
- ✅ Determine which sampling strategies are most effective
- ✅ Optimize resource allocation
- ✅ Evaluate intervention effectiveness
- ✅ Identify program improvements needed

---

## Limitations & Considerations

### What We CANNOT Determine from This Data:

1. **Outbreak Causation**
   - This data shows lab results from facility sampling, NOT clinical illness cases
   - Cannot link to specific foodborne illness outbreaks without CDC/state health department data
   - Cannot determine consumer exposure or illness burden

2. **Geographic Precision**
   - State-level location only (no city/address data)
   - Cannot create precise facility location maps
   - Cannot analyze urban vs rural patterns

3. **Supply Chain & Distribution**
   - No data on product distribution networks
   - Cannot track where contaminated products were shipped
   - Cannot identify common suppliers

4. **Root Cause Analysis**
   - No data on facility practices, sanitation, or corrective actions
   - Cannot determine WHY contamination occurred
   - Cannot evaluate specific intervention effectiveness

5. **Economic Impact**
   - No data on recalls, product destruction, or economic losses
   - Cannot assess financial burden of contamination

6. **Historical Context**
   - Only FY2025 data available (one year)
   - Cannot analyze long-term trends or year-over-year changes
   - Limited temporal pattern detection

### External Data Sources That Would Enhance Analysis:

1. **CDC PulseNet / NCBI Pathogen Detection**
   - Link lab strains to clinical illness cases
   - Identify actual outbreaks vs environmental contamination

2. **USDA Enforcement Database**
   - Recalls, regulatory actions, facility suspensions
   - Connect contamination to regulatory outcomes

3. **Geographic/Demographic Data**
   - Facility addresses for precise mapping
   - Population density for risk normalization
   - State geocoding for better visualization

4. **Supply Chain Data**
   - Product distribution networks
   - Common ingredient suppliers
   - Cross-contamination pathways

5. **Historical Sampling Data**
   - FY2014-2024 for trend analysis
   - Long-term facility compliance tracking

---

## Recommended Dashboard Technologies

### Option 1: Python + Plotly Dash (Recommended)
**Pros:**
- Fully customizable interactive dashboards
- Excellent mapping libraries (Plotly, Folium)
- Can handle large datasets efficiently
- Easy to deploy (local or web)
- Strong statistical analysis capabilities with pandas/numpy

**Cons:**
- Requires Python knowledge
- More development time than BI tools

### Option 2: Python + Streamlit
**Pros:**
- Rapid development
- Very easy to create interactive apps
- Good for prototyping
- Minimal code required

**Cons:**
- Less customizable than Dash
- Limited complex layout options

### Option 3: Tableau / Power BI
**Pros:**
- No coding required
- Beautiful out-of-the-box visualizations
- Easy sharing and collaboration

**Cons:**
- Expensive licensing
- Less flexible for custom analyses
- May struggle with large JSON files

### Option 4: JavaScript + D3.js + Leaflet
**Pros:**
- Highly interactive web-based dashboard
- Beautiful custom visualizations
- Best mapping capabilities

**Cons:**
- Requires JavaScript expertise
- More development time
- Complex data processing

---

## Recommended Implementation: Python + Plotly Dash

**Rationale:**
- Best balance of power, flexibility, and development speed
- Excellent data manipulation with pandas
- Rich visualization library (Plotly)
- Built-in interactivity (dropdowns, date pickers, hover tooltips)
- Can easily add mapping with Plotly's choropleth maps
- Easy to extend with additional analysis modules

---

## Next Steps (Phase 3)

Create `main.py` with modular structure:

```
listeria-tracker/
├── main.py                    # Dashboard entry point
├── data/
│   └── loader.py             # Data loading and caching
├── analysis/
│   ├── statistics.py         # Statistical analysis functions
│   └── clustering.py         # Outbreak detection algorithms
├── visualization/
│   ├── maps.py              # Geographic visualizations
│   ├── timeseries.py        # Temporal charts
│   └── tables.py            # Data tables and scorecards
└── docs/
    ├── 1-research.md
    └── 1-research-findings.md
```

**Implementation Plan Details:** Awaiting approval to create `docs/2-plan.md`
