# FSIS Recall Data Analysis (2025)
## Animal Product Recalls vs. Plant-Based Products

**Document Date:** March 16, 2026
**Analysis Type:** Exploratory - Recall Summary Analysis
**Data Period:** Calendar Year 2025

---

## Executive Summary

**Key Finding:** The FSIS Recall Summary for 2025 contains **exclusively animal product recalls** - no plant-based products are included in this dataset. This represents a **critical data gap** for comparing animal vs. plant contamination rates.

**Total Recalls:** 42
**Total Pounds Recalled:** 71,420,721 lbs (~35,710 tons)
**Product Types:** 100% meat, poultry, and fish - 0% plant-based

---

## Data Sources

### Primary Source
- **File:** `data/fsisRecallSummary2025.xlsx`
- **Description:** FSIS official recall summary for calendar year 2025
- **Sheet:** CY2025 Recall Summary
- **Format:** Aggregate summary (not individual recall records)
- **Records:** 29 rows of summary statistics
- **Limitation:** Contains only FSIS-regulated products (meat, poultry, fish)

### Scope Limitation
**FSIS Jurisdiction:** FSIS (Food Safety and Inspection Service) regulates:
- ✓ Meat products (beef, pork, lamb)
- ✓ Poultry products (chicken, turkey, duck)
- ✓ Processed meat/poultry products
- ✓ Egg products (processed)

**FDA Jurisdiction:** FDA (Food and Drug Administration) regulates:
- ✗ Fresh produce (fruits, vegetables)
- ✗ Grains and grain products
- ✗ Dairy products
- ✗ Seafood (except catfish/siluriformes)
- ✗ Plant-based meat alternatives

**Implication:** This dataset **cannot** answer the question "Are animal products recalled more than plant products?" because plant products fall under different regulatory authority.

---

## Recall Overview

### Total Recalls (CY2025)

| Metric | Value |
|--------|-------|
| **Total Recalls** | 42 |
| **Total Pounds** | 71,420,721 |
| **Average Recall Size** | 1,700,493 lbs |

---

## Recalls by Severity Class

| Class | Number | Pounds | % of Total Recalls | % of Total Pounds |
|-------|--------|--------|-------------------|-------------------|
| **Class I** (Serious health hazard) | 38 | 71,049,346 | 90.5% | 99.5% |
| **Class II** (Temporary health risk) | 2 | 15,691 | 4.8% | 0.02% |
| **Class III** (Unlikely to cause harm) | 2 | 355,684 | 4.8% | 0.5% |

**Key Insight:** 90.5% of recalls were Class I (most serious), accounting for 99.5% of recalled pounds.

---

## Recalls by Reason

| Reason | Count | Pounds | % of Recalls | Ranking |
|--------|-------|--------|--------------|---------|
| **Extraneous Material** | 13 | 69,619,536 | 31.0% | #1 |
| **Undeclared Allergen** | 9 | 744,489 | 21.4% | #2 |
| **Produced without Inspection** | 7 | 187,026 | 16.7% | #3 |
| **Import Violation** | 5 | 32,842 | 11.9% | #4 |
| **Listeria monocytogenes** | 4 | 459,497 | 9.5% | #5 |
| **Unapproved Substance** | 2 | 231,060 | 4.8% | #6 |
| **Shiga Toxin-Producing E. coli** | 1 | 2,855 | 2.4% | #7 |
| **Misbranding** | 1 | 143,416 | 2.4% | #8 |
| **Total** | 42 | 71,420,721 | 100% | |

### Analysis by Recall Reason

**1. Extraneous Material (Physical Contamination) - 31% of Recalls**
- **Examples:** Metal, plastic, glass in products
- **Pounds:** 69.6 million lbs (97.5% of all recalled pounds!)
- **Concern:** Manufacturing/processing control issues
- **Note:** Dominates recall volume - likely one or two very large recalls

**2. Undeclared Allergen - 21.4% of Recalls**
- **Examples:** Milk, eggs, soy, wheat not listed on labels
- **Pounds:** 744,489 lbs
- **Concern:** Labeling/formulation control issues
- **Impact:** Serious for allergic consumers

**3. Produced without Inspection - 16.7% of Recalls**
- **Examples:** Products made at uninspected facilities
- **Pounds:** 187,026 lbs
- **Concern:** Regulatory compliance issue
- **Impact:** Unknown food safety status

**4. Pathogen Contamination - 11.9% of Recalls (Combined)**
- **Listeria monocytogenes:** 4 recalls, 459,497 lbs
- **E. coli (STEC):** 1 recall, 2,855 lbs
- **Total Pathogen Recalls:** 5 out of 42 (11.9%)
- **Significance:** Pathogens are a **minority** of recalls by count, but represent serious health risks

---

## Recalls by Species (Product Type)

| Species | Count | Pounds | % of Recalls | Average Size (lbs) |
|---------|-------|--------|--------------|-------------------|
| **Mixed*** | 10 | 62,273,005 | 23.8% | 6,227,301 |
| **Swine (Pork)** | 11 | 3,010,483 | 26.2% | 273,680 |
| **Chicken** | 9 | 5,313,865 | 21.4% | 590,429 |
| **Beef** | 7 | 324,025 | 16.7% | 46,289 |
| **Siluriformes (Catfish)** | 3 | 125,561 | 7.1% | 41,854 |
| **Turkey** | 1 | 367,812 | 2.4% | 367,812 |
| **Sheep/Lamb** | 1 | 5,970 | 2.4% | 5,970 |
| **Total** | 42 | 71,420,721 | 100% | 1,700,493 |

*Mixed refers to recalls containing multiple meat/poultry species

### Species Analysis

**Findings:**
1. **Pork products** have the most recalls by count (11), but **Mixed** products dominate by weight (62.3M lbs)
2. **Mixed products** have the largest average recall size (6.2M lbs) - suggests multi-product manufacturing issues
3. **Beef** has relatively few recalls despite high consumption
4. **No plant-based products** appear in any category

**Recall Rate vs. Consumption:**
- Cannot calculate true "recall rate per pound consumed" without consumption data
- See [`consumptionDataAnalysis.md`](consumptionDataAnalysis.md) for consumption patterns
- **Hypothesis:** Pork's high recall count (11) may correlate with ready-to-eat processing (deli meats, sausages)

---

## Pathogen-Specific Deep Dive

### Listeria monocytogenes (4 Recalls)

| Metric | Value |
|--------|-------|
| **Recalls** | 4 |
| **Pounds** | 459,497 |
| **% of Total Recalls** | 9.5% |
| **Severity** | Class I (all) |

**Context from Lab Sampling Data:**
- Lab sampling data ([`gcpLabJoinedAnalysis.md`](gcpLabJoinedAnalysis.md)) shows:
  - RTE Chicken: 0.25-1.81% pathogen detection
  - RTE Pork Sausage: 0.84% pathogen detection
- **Correlation:** Listeria recalls align with known RTE contamination risks

**Species Likely Affected:**
- Cannot determine from summary data which species had Listeria
- Most likely: Ready-to-eat meats (deli meats, hot dogs, sausages)

### E. coli STEC (1 Recall)

| Metric | Value |
|--------|-------|
| **Recalls** | 1 |
| **Pounds** | 2,855 |
| **Severity** | Class I |

**Context:**
- E. coli typically associated with:
  - Ground beef (most common)
  - Raw beef products
- Small recall size suggests localized issue

---

## Critical Data Gaps

### 1. No Plant-Based Product Data ❌

**Problem:** FSIS only regulates meat/poultry/fish

**Missing:**
- Vegetable recalls (e.g., lettuce, spinach)
- Fruit recalls (e.g., cantaloupes, berries)
- Grain product recalls
- Plant-based meat alternatives

**Impact:** **Cannot answer the research question:** "Are animal products recalled more than plant products?"

**Recommendation:** Obtain FDA recall data for produce/plant products to enable fair comparison

---

### 2. No Ready-to-Eat vs. Raw Classification ⚠️

**Problem:** Summary doesn't distinguish RTE from raw products

**Example:**
- "Chicken" recalls could be:
  - Raw chicken breasts → E. coli/Salmonella concern
  - RTE chicken strips → Listeria concern
  - These are **not comparable** product categories

**Impact:** Cannot perform the requested "RTE vs. RTE, raw vs. raw" comparison

**Recommendation:** Obtain detailed individual recall records from FSIS with product descriptions

---

### 3. No Individual Recall Records ⚠️

**Problem:** File contains only aggregate statistics

**Missing:**
- Individual recall dates
- Establishment names/numbers
- Specific product names
- Distribution information
- Root cause details

**Impact:** Cannot link recalls to:
- Establishments in GCP data ([`gcpArchiveFy2024.xlsx`](../data/gcpArchiveFy2024.xlsx))
- Contamination rates in lab sampling data
- Specific commercial practices

**Recommendation:** Obtain FSIS "Recall Case Archive" database with individual recall records

---

## Comparison with Lab Sampling Data

### Pathogen Detection vs. Recalls

| Data Source | Listeria Detection | Salmonella Detection | E. coli Detection |
|-------------|-------------------|---------------------|-------------------|
| **Lab Sampling (FY2025)** | 0.25-1.81% positive rate | Tracked in data | Tracked in data |
| **Recalls (CY2025)** | 4 recalls (9.5%) | Not mentioned | 1 recall (2.4%) |

**Interpretation:**
- Lab sampling finds pathogens at low rates (< 2%)
- Recalls are triggered when contaminated products reach consumers
- **Not all positive lab samples result in recalls** (sampling is preventive)

**Recall Trigger Process:**
1. **Pre-distribution sampling** → Product held, not released (no recall)
2. **Post-distribution detection** → Product already shipped → **Recall**

**Implication:** Recalls represent **failures in the preventive system**

---

## Temporal Context

### Data Period Alignment

| Dataset | Time Period | Notes |
|---------|-------------|-------|
| **Recall Summary** | CY2025 (Jan-Dec 2025) | Summary format |
| **Lab Sampling** | FY2025 (Oct 2024-Sep 2025) | Detailed records |
| **GCP Inspections** | FY2024 (Oct 2023-Sep 2024) | One year earlier |
| **Consumption Data** | 2017-2018 | **8 years outdated** |

**Alignment Issue:** Cannot correlate 2025 recalls with 2017-2018 consumption patterns

---

## Insights for Dashboard

### What This Data CAN Support:

✅ **Animal Product Recall Breakdown by Species**
- Show pie chart: Pork (26%), Chicken (21%), Beef (17%), etc.
- Annotation: "FSIS-regulated products only"

✅ **Recall Reasons Distribution**
- Show bar chart: Extraneous Material (31%), Allergens (21%), Pathogens (12%)
- Insight: "Most recalls are NOT pathogen-related"

✅ **Pathogen Recall Count**
- Listeria: 4 recalls
- E. coli: 1 recall
- Compare to lab sampling positive rates

✅ **Severity Distribution**
- 90.5% Class I (serious hazards)
- Emphasize: Most meat recalls are serious

---

### What This Data CANNOT Support:

❌ **Animal vs. Plant Recall Comparison**
- Reason: No plant product data (FDA jurisdiction)
- Alternative: Acknowledge limitation, note 100% animal in FSIS data

❌ **RTE vs. Raw Comparison**
- Reason: No product category details in summary
- Alternative: Use lab sampling data as proxy

❌ **Establishment-Level Correlation**
- Reason: No establishment identifiers
- Alternative: Use GCP+Lab joined data instead

❌ **Temporal Trends**
- Reason: Only one year of summary data
- Alternative: State this is a snapshot of 2025

---

## Recommendations

### Immediate Actions (Dashboard)

1. **Document Data Limitation Prominently**
   ```
   "Note: Plant-based products fall under FDA jurisdiction and are
   not included in FSIS recall data. This analysis covers meat,
   poultry, and fish products only."
   ```

2. **Use Existing Data Strengths**
   - Focus on species breakdown (pork, chicken, beef)
   - Highlight pathogen recalls (Listeria, E. coli)
   - Show recall reasons distribution

3. **Cross-Reference with Lab Data**
   - Correlate 4 Listeria recalls with RTE contamination rates
   - Show that recalls represent failures in preventive system

---

### Future Data Collection

**Priority 1: FDA Recall Data (Plant Products)**
- Source: FDA CFSAN (Center for Food Safety and Applied Nutrition)
- Data: Produce recalls, plant-based product recalls
- Enable: True animal vs. plant comparison

**Priority 2: FSIS Individual Recall Records**
- Source: FSIS Recall Case Archive
- URL: https://www.fsis.usda.gov/recalls
- Data: Individual recalls with:
  - Establishment numbers (linkable to GCP data!)
  - Product descriptions (RTE vs. raw classification)
  - Distribution info
  - Root cause analysis

**Priority 3: Historical Recall Data**
- Years: 2020-2024
- Enable: Temporal trend analysis
- Question: "Are recalls increasing or decreasing?"

---

## Statistical Summary

### Descriptive Statistics

**Central Tendency:**
- Mean recall size: 1,700,493 lbs
- Median recall size: [Cannot calculate from summary data]
- Mode species: Pork (11 recalls)

**Distribution:**
- Highly skewed by "Extraneous Material" category (97.5% of pounds)
- Likely one mega-recall driving the total

**Recall Rate (Rough Estimate):**
- US meat/poultry production: ~100 billion lbs/year
- Recalled: 71.4 million lbs
- **Rate: 0.07% of production**

---

## Plant-Based Product Contamination Gap

### The Missing Picture

**What We Know:**
- ✓ Animal product recalls: 42 in CY2025 (FSIS data)
- ❌ Plant product recalls: Unknown (need FDA data)

**Why This Matters:**
- **Research Question:** "Do factory-produced animal products have higher contamination than plant products?"
- **Current State:** Can only show animal contamination, not compare
- **Impact on Conclusions:** **Cannot make comparative claims without plant data**

### Alternative Approach: Lab Sampling vs. Plant Products

**Hypothesis Test:**
- **H0:** Animal and plant products have equal contamination rates
- **Current Evidence:**
  - Animal pathogen detection: 0.25-1.81% (lab sampling)
  - Plant pathogen detection: **No data available**

**Conclusion:** **Analysis blocked by missing data**

---

## Dashboard Story Arc Suggestion

Given the data limitations, focus the dashboard narrative on:

1. **"Animal Product Safety Landscape"**
   - Present FSIS recall data as-is
   - Show species breakdown, recall reasons
   - Highlight pathogen recalls (Listeria, E. coli)

2. **"Preventive System Performance"**
   - Show lab sampling detection rates (< 2%)
   - Show recall rate (0.07% of production)
   - Message: "Most contamination caught before distribution"

3. **"Commercial Practices Impact"**
   - Link GCP violations to contamination risk
   - Use establishment-level correlation from [`gcpLabJoinedAnalysis.md`](gcpLabJoinedAnalysis.md)
   - Message: "Better animal welfare correlates with lower contamination"

4. **"Data Gaps and Future Research"**
   - Acknowledge missing plant product data
   - State this limits comparative conclusions
   - Call for comprehensive food safety data across all categories

---

## Key Findings Summary

1. **All Recalls are Animal Products:** 100% of FSIS recalls involve meat, poultry, or fish
2. **Pork Leads by Count:** 11 recalls (26.2% of total)
3. **Extraneous Material Dominates:** 31% of recalls, 97.5% of recalled pounds
4. **Pathogen Recalls are Minority:** Only 11.9% of recalls (5 out of 42)
5. **Most Recalls are Serious:** 90.5% are Class I (serious health hazard)
6. **Critical Data Gap:** No plant-based product data available for comparison

---

## Methodology

**Analysis Script:** [`scripts/analyzeRecallData.py`](../scripts/analyzeRecallData.py)

**Analysis Steps:**
1. Loaded FSIS Recall Summary Excel file
2. Identified data structure (summary format, not records)
3. Extracted recall counts by reason, species, and class
4. Searched for animal vs. plant product classifications
5. Cross-referenced with lab sampling and GCP data
6. Documented data gaps and limitations

**Tools:**
- Python 3, pandas, openpyxl
- Excel data parsing

**Date Performed:** March 16, 2026

---

## References

### Data Sources
- Primary: `data/fsisRecallSummary2025.xlsx`
- Related: `data/labSamplingRteFy2025.json`, `data/gcpArchiveFy2024.xlsx`

### Related Documentation
- [`consumptionDataAnalysis.md`](consumptionDataAnalysis.md) - Food consumption patterns
- [`gcpLabJoinedAnalysis.md`](gcpLabJoinedAnalysis.md) - Establishment-level contamination correlation
- [`porkSausageAnalysis.md`](porkSausageAnalysis.md) - Pork product contamination details

### External References
- FSIS Recall Procedures: https://www.fsis.usda.gov/recalls
- FSIS Directive 8080.1: Recall of Meat and Poultry Products
- FDA Recalls Database: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-16 | 1.0 | Initial analysis of CY2025 recall summary data |
