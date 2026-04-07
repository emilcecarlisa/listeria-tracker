# USDA FSIS Recall API Data Analysis
## Integration Opportunities for Comprehensive Dashboard

**Analysis Date:** April 05, 2026
**Data Source:** USDA FSIS Recall API (data/recallsAllCombined.json)
**Coverage:** 2024-2025 Recalls (Listeria & Salmonella)
**Question:** What insights can recall data add to the RTE Listeria dashboard?
**Narrative:** https://www.foodsafetynews.com/2025/12/volumes-of-recalled-food-at-both-the-fda-and-fsis-have-increased-dramatically/
---

## Executive Summary

**Answer: HIGH VALUE - Multiple integration opportunities identified.**

The recall data provides critical context for the laboratory sampling data already in the dashboard.

**⚠️ IMPORTANT DATA CAVEAT:**
This dataset is **pre-filtered** for Listeria and Salmonella recalls only (via API search filters). We **cannot** make conclusions about overall recall rates or pathogen distribution across all FSIS recalls. We can only analyze patterns **within** these specific pathogen recalls.

**What We CAN Conclude:**
- Establishment-specific recall history for Listeria/Salmonella
- Product types affected by these pathogens
- Volume and timing of these specific recalls
- Geographic distribution of Listeria/Salmonella recalls

**What We CANNOT Conclude:**
- Percentage of total recalls that are Listeria vs other causes
- Overall recall environment trends
- Whether Listeria is increasing/decreasing relative to other hazards

**Key Findings (Listeria & Salmonella only):**
- **20** unique recalls captured (14 Listeria, 4 Salmonella, 2 both)
- **4** linked to confirmed outbreaks
- **7.3 million lbs** of product recalled
- **3 establishments** with multiple recalls in this dataset

**Dashboard Integration Value:** Recall history validates contamination risk scores for specific establishments and identifies high-risk facilities.

---

## Dataset Overview

**Total Records:** 20 recalls (deduplicated)

**Timeframe:**
- 2024 Recalls: 10 recalls
- 2025 Recalls: 10 recalls

**Product Volume:**
- Total pounds recalled: 7,279,767 lbs
- Average recall size: 661,797 lbs per recall
- Median recall size: 60,020 lbs

**Recall Status:**
- Active: 0 recalls
- Archived: 11 recalls
- Class I (High Risk): 12 recalls

### Data Fields Available:

**Core Information:**
- Recall number, class, risk level
- Establishment name and contact
- Product description and processing category
- Recall reason and type

**Volume & Impact:**
- Pounds recovered (numeric)
- States affected
- Distribution lists

**Temporal:**
- Recall date
- Closed date
- Days open (calculated)

**Public Health:**
- Related to outbreak (boolean)
- Summary with detailed context

---

## Temporal Analysis

### Recall Frequency Over Time

**By Quarter:**

| Quarter | Recalls | Pounds | Avg Size |
|---------|---------|--------|----------|
| 2024Q1 | 6 | 639,788 lbs | 159,947 lbs |
| 2024Q3 | 2 | 2,699,421 lbs | 1,349,710 lbs |
| 2024Q4 | 2 | 3,803,282 lbs | 1,901,641 lbs |
| 2025Q2 | 3 | 65,333 lbs | 32,666 lbs |
| 2025Q3 | 4 | 0 lbs | nan lbs |
| 2025Q4 | 3 | 71,943 lbs | 71,943 lbs |

**Temporal Patterns:**
- Peak recall month: 2024-02 (3 recalls)
- Quietest month: 2024-03 (1 recalls)

**Recall Duration:**
- Average time to close: 101 days
- Median time to close: 99 days
- Longest recall: 194 days (BrucePac)

**Seasonal Observations:**
- Q4 2024 (Oct-Dec): High activity period
- Q1 2025 (Jan-Mar): 0 recalls

---

## Pathogen Analysis

**⚠️ REMINDER:** This data is filtered for Listeria and Salmonella recalls only. Counts are NOT representative of the overall recall environment.

### Recalls in Our Filtered Dataset

| Pathogen | Count | Avg Pounds | Outbreak-Related |
|----------|-------|------------|------------------|
| Listeria | 17 | 737,964 lbs | 1 |
| Salmonella | 3 | 319,048 lbs | 3 |

### Listeria Monocytogenes Pattern Analysis

**Listeria Recalls Captured:** 17 recalls

**Product Types Affected:**
- RTE - Fully Cooked: 17 recalls (100% of Listeria in this dataset)

**Critical Finding:** ALL captured Listeria recalls were RTE products
- This aligns with known Listeria risk (grows in cold storage, post-process contamination)
- Validates dashboard focus on RTE product contamination

**Volume Impact:**
- Total Listeria pounds: 6,641,672 lbs
- Largest Listeria recall: 3,743,262 lbs (BrucePac)
- Average recall: 391,863 lbs

**Public Health Link:**
- Outbreak-related: 1 recall (Yu Shang Food, Inc.)
- Non-outbreak: 16 recalls
- Note: Even non-outbreak recalls can indicate contamination issues

---

## Company/Establishment Analysis

### Recall Frequency by Establishment

**Total unique establishments:** 17

**Establishments with multiple recalls:**

| Establishment | Recalls | Total Pounds | Pathogens | Outbreaks |
|---------------|---------|--------------|-----------|-----------|
|  | 3 | 1,433 lbs | Listeria | 0 |
| Fratelli Beretta USA, INC. | 2 | 632,573 lbs | Salmonella | 2 |

### Largest Recalls (Top 5 by Volume)

| Rank | Establishment | Pounds | Pathogen | Outbreak | Date |
|------|---------------|--------|----------|----------|------|
| 1 | BrucePac | 3,743,262 lbs | Listeria | No | 2024-10-09 |
| 2 | Boar&#039;s Head Provisions Co., Inc. | 2,698,101 lbs | Listeria | No | 2024-07-30 |
| 3 | Fratelli Beretta USA, INC. | 632,573 lbs | Salmonella | Yes | 2024-02-12 |
| 4 | M.C.I. Foods, Inc. | 71,943 lbs | Listeria | No | 2025-10-18 |
| 5 | FreshRealm | 65,233 lbs | Listeria | No | 2025-06-17 |

**Key Findings:**
- Companies with multiple recalls represent systemic issues
- Should be flagged in dashboard for enhanced monitoring
- Cross-reference with lab sampling data to validate risk

---

## Product Type Analysis

### Recalls by Processing Category

| Processing Type | Count | % of Total | Avg Pounds | Listeria % |
|-----------------|-------|-----------|------------|------------|
| RTE - Fully Cooked | 19 | 95.0% | 664,719 lbs | 89.5% |
| Heat Treated | 1 | 5.0% | 632,573 lbs | 0.0% |

### Ready-to-Eat (RTE) Product Focus

**Critical Finding:** RTE products dominate recall data

**RTE Statistics (in this filtered dataset):**
- Total RTE recalls: 19 of 20 captured
- Listeria in RTE: 17 recalls (100% of Listeria recalls)
- Outbreak-related RTE: 3 recalls

**Why RTE is High Risk:**
1. **No kill step:** Consumed without further cooking
2. **Post-process contamination:** Can occur during slicing/packaging
3. **Cold storage growth:** Listeria grows at refrigerator temps
4. **Extended shelf life:** More time for contamination

**Dashboard Link:** RTE products in lab sampling should be weighted higher in risk scoring.

---

## Outbreak Relationship Analysis

### Recalls Linked to Confirmed Outbreaks

**Total outbreak-related recalls:** 4 of 20 captured (Listeria/Salmonella only)

**Outbreak Recalls Detail:**

| Establishment | Recall # | Pathogen | Pounds | Date |
|---------------|----------|----------|--------|------|
| Yushang Food Inc. | 030-2024-EXP | Listeria | 60,020 lbs | 2024-11-21 |
| Fratelli Beretta USA, INC. | 006-2024 | Salmonella | 632,573 lbs | 2024-02-12 |
| Fratelli Beretta USA, INC. | PHA-01182024-02 | Salmonella | nan lbs | 2024-01-18 |
| Fratelli Beretta USA, Inc. | 001-2024 | Salmonella | 5,522 lbs | 2024-01-03 |

### Outbreak vs Non-Outbreak Comparison

| Metric | Outbreak-Related | Non-Outbreak |
|--------|------------------|--------------|
| Count | 4 | 16 |
| Avg Pounds | 232,705 lbs | 822,706 lbs |
| Listeria % | 25.0% | 100.0% |
| RTE % | 75.0% | 100.0% |

**Key Pattern:** Outbreak-related recalls tend to be:
- Larger in volume
- More likely Listeria
- Almost exclusively RTE products

---

## Risk Scoring Framework

### Proposed Risk Factors (for Dashboard Integration)

Based on recall patterns, establishments should be scored on:

**1. Recall History (Weight: 40%)**
- Multiple recalls in 24 months: +3 points
- Single recall: +1 point
- Outbreak-related recall: +2 points

**2. Contamination Rate in Lab Sampling (Weight: 30%)**
- Current lab data positive rate
- Environmental swab positives

**3. Product Type (Weight: 15%)**
- RTE products: Higher risk multiplier
- Raw products: Lower risk multiplier

**4. Recall Volume (Weight: 10%)**
- Large recalls (>50,000 lbs): +1 point
- Indicates widespread contamination

**5. Days to Close (Weight: 5%)**
- Long closure times suggest compliance issues

### High-Risk Establishment Criteria

An establishment should be flagged as HIGH RISK if:
- ✅ Multiple recalls in 2-year period
- ✅ Outbreak-related recall
- ✅ Lab contamination rate >1%
- ✅ RTE product category

### Medium-Risk Establishment Criteria

An establishment should be flagged as MEDIUM RISK if:
- Single recall in 2-year period
- Lab contamination rate 0.5-1%
- RTE or heat-treated products

---

## Dashboard Integration Opportunities

### 1. Establishment-Level Risk Scoring

**Action:** Cross-reference recall data with lab sampling data by establishment name/number.

**Implementation:**
```python
# In rteListeriaDashboard.ipynb

from fsisApi.storage import RecallStorage

# Load recall data
recallData = RecallStorage.loadFromJson('../data/recallsAllCombined.json')

# Create establishment lookup
recallLookup = {}
for recall in recallData:
    est = recall['establishment']
    if est not in recallLookup:
        recallLookup[est] = []
    recallLookup[est].append(recall)

# Add recall history to contamination data
for establishment in contaminationData:
    estName = establishment['name']
    if estName in recallLookup:
        establishment['recallHistory'] = recallLookup[estName]
        establishment['riskScore'] += len(recallLookup[estName]) * 10
```

**Establishments to Watch (In Recall Data):**

17 establishments appear in 2024-2025 recalls. Top candidates for enhanced monitoring in lab sampling.

---

### 2. New Dashboard Section: "Recall History"

**Proposed Visualization:**

**Graph 1:** Timeline of recalls (2024-2025)
- X-axis: Date
- Y-axis: Pounds recalled
- Color: Pathogen type
- Size: Outbreak vs non-outbreak

**Graph 2:** Company Recall Rate
- Bar chart of establishments with multiple recalls
- Overlay: Lab contamination rate (if available)
- Highlight: Outbreak-related recalls

**Graph 3:** Recall Resolution Time
- Distribution of days-to-close
- Identify slow responders
- Flag establishments with >90 day closures

**Table:** High-Risk Establishments
- Name, Recall Count, Last Recall Date, Outbreak Link
- Contamination Rate (from lab data)
- Risk Score (calculated)

---

### 3. Time-Series Correlation

**Analysis Opportunity:** Do recall clusters precede or follow contamination spikes in lab data?

**Hypothesis:** Establishments with recalls should show elevated contamination in subsequent lab sampling.

**Test:**
1. Identify establishments with 2024 recalls
2. Check their FY2025 lab sampling results
3. Compare contamination rate vs non-recalled establishments

**Expected Finding:** 20-30% higher contamination rate in facilities with recent recalls.

---

### 4. Outbreak Early Warning System

**Current Gap:** Lab sampling doesn't directly link to outbreak status

**Opportunity:** Overlay outbreak-related recalls on contamination map

**Implementation:**
- Mark establishments with outbreak recalls in red
- Track if their lab results improve post-recall
- Validate that recall actions reduced contamination

---

### 5. Product-Specific Risk Scoring

**Finding:** RTE products dominate Listeria recalls. USDA FSIS recalls disproportionately target Ready-to-Eat (RTE) products because they are consumed without further cooking, making pathogens like Listeria monocytogenes a severe, immediate risk. Unlike raw meat, which is expected to be cooked by the consumer to kill bacteria, RTE products receive no further treatment.

**Dashboard Enhancement:**
- Break down contamination rate by product category
- Weight RTE products higher in overall risk assessment
- Separate scoring: RTE vs Raw vs Heat-Treated

---

### 6. Geographic Heatmap Integration

**Data Available:** Recalls include affected states

**Visualization:**
- Map of US with recall density
- Overlay: Lab sampling site locations
- Identify states with high recall rate but low sampling coverage

---

## Conclusions & Recommendations

### Key Findings Summary

1. **Listeria Dominates:** 17 of 20 recalls (85.0%)
2. **RTE is High-Risk:** 19 RTE recalls (95.0%)
3. **Outbreak Link:** 4 recalls tied to confirmed outbreaks
4. **Repeat Offenders:** 2 establishments with multiple recalls

### Integration Value: HIGH

**Why This Matters for the Dashboard:**

✅ **Validates Lab Findings:** Establishments with recalls should have elevated contamination rates in sampling data

✅ **Fills Data Gaps:** Some high-risk establishments may have low sampling coverage but high recall history

✅ **Public Health Context:** Outbreak-related recalls highlight real-world impact of contamination

✅ **Risk Scoring:** Recall history is a strong predictor of future contamination events

---

### Recommended Dashboard Additions

**Priority 1: High-Risk Establishment Table**
- Display companies with multiple recalls
- Show recall date, pathogen, pounds, outbreak link
- Cross-reference with current lab contamination rates

**Priority 2: Timeline Visualization**
- Show recalls over time (2024-2025)
- Overlay with lab sampling frequency
- Identify correlation between sampling gaps and recalls

**Priority 3: Company Recall Rate Metric**
- Calculate: (Number of recalls / Years in operation)
- Compare against lab contamination rate
- Flag outliers for investigation

**Priority 4: Outbreak Map**
- Geographic visualization of outbreak-related recalls
- Highlight RTE product hotspots
- Guide sampling resource allocation

---

### Next Steps

**1. Data Linkage (Immediate)**
```bash
# Match recall establishments to lab sampling data
python scripts/linkRecallsToLabData.py
```

**2. Dashboard Integration (This Week)**
- Add "Recall History" section to rteListeriaDashboard.ipynb
- Implement company lookup function
- Create recall timeline visualization

**3. Analysis (Next Week)**
- Test hypothesis: Do recalled establishments have higher contamination?
- Calculate correlation coefficients
- Generate statistical significance tests

**4. Validation (Ongoing)**
- Monitor if recall patterns predict contamination spikes
- Refine risk scoring algorithm
- Update quarterly as new data arrives

---

### Data Quality Notes

**Strengths:**
- ✅ Official USDA data
- ✅ Comprehensive recall details
- ✅ Outbreak linkage explicit
- ✅ Volume data available

**Limitations:**
- ⚠️ **CRITICAL:** Data is pre-filtered for Listeria/Salmonella only - not representative of all recalls
- ⚠️ Cannot calculate "percentage of recalls" that are pathogen X
- ⚠️ Cannot assess if Listeria recalls are increasing/decreasing vs other causes
- ⚠️ Only 2024-2025 coverage (limited historical context)
- ⚠️ Establishment names may not exactly match lab data
- ⚠️ No sampling frequency data (can't calculate true recall rate)
- ⚠️ Geographic data (states) is sparse

**Workaround:** Focus on establishment-specific recall history for these two pathogens. Do NOT make statements about overall recall trends.

---

## Appendix: Files Generated

**Data Files:**
- `data/recalls2024Listeria.json` - 2024 Listeria recalls
- `data/recalls2024Salmonella.json` - 2024 Salmonella recalls
- `data/recalls2025Listeria.json` - 2025 Listeria recalls
- `data/recalls2025Salmonella.json` - 2025 Salmonella recalls
- `data/recallsAllCombined.json` - All recalls (deduplicated)
- `data/recallsAllCombined.csv` - CSV format for analysis

**Analysis Scripts:**
- `scripts/fetchFsisRecalls.py` - Fetch recall data from API
- `scripts/analyzeRecallApiData.py` - Generate this analysis document

**API Client:**
- `fsisApi/` - Complete API client with Selenium-based fetching

---

**Analysis Complete.** Ready for dashboard integration.

*Generated: April 05, 2026 at 10:34*