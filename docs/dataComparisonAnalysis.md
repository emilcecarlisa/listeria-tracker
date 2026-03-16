# Data Comparison Analysis: Testing the "Popular Foods Contamination" Hypothesis

## Executive Summary

**Research Question:** Is there an increase in contamination or recalls that can be traced to the types of foods that are popularly sold?

This document compares two datasets to determine which provides stronger evidence for testing this hypothesis:
1. **USDA FSIS Recall Data** (reactive, public health actions)
2. **USDA FSIS Lab Sampling Data** (proactive, systematic surveillance)

**TL;DR Recommendation:** **Lab contamination data is superior** for testing this hypothesis due to systematic sampling, statistical baselines, and larger sample sizes. However, **combining both datasets** provides the most compelling evidence.

---

## Dataset Comparison

### Dataset 1: USDA FSIS Recall Data

**Example Structure:**
```
Recall ID: 003-2026
Classification: High - Class I
Reason: Product Contamination (E. coli O145)
Company: CS Beef Packers, LLC
Status: Active
Date Range: Feb 11, 2026 - Current
Distribution: California, Idaho, Oregon
Volume: 22,912 pounds
Products: Ground Beef (73% lean, 81% lean)
```

**Strengths:**
- ✅ **Real consumer impact**: Shows products that actually reached market
- ✅ **Severity classification**: Class I/II/III indicates public health risk
- ✅ **Geographic distribution**: Multi-state impact visible
- ✅ **Specific products/brands**: "Fire River Farms Classic Beef" - actual market products
- ✅ **Volume data**: Pounds recalled = proxy for market size
- ✅ **Temporal precision**: Exact recall dates and "Use By" dates

**Weaknesses:**
- ❌ **Selection bias**: Only problems that were caught and deemed serious enough
- ❌ **Reactive dataset**: Contamination already occurred and reached consumers
- ❌ **Small sample size**: ~50-200 recalls/year vs 27,000+ lab samples
- ❌ **No statistical baseline**: No data on non-recalled products
- ❌ **Reporting bias**: High-profile products/companies more likely to recall
- ❌ **Detection lag**: Recalls happen weeks/months after contamination
- ❌ **Missing "popularity" metric**: No sales data, consumption rates, or market share

**Data Available:**
- Recall date, classification, pathogen type
- Product description, brand names
- Distribution states
- Establishment information
- Volume recalled (pounds)

---

### Dataset 2: USDA FSIS Lab Sampling Data (Current Dataset)

**Structure:**
- 27,211 samples from 2,364 establishments
- Both positive (208 Listeria, 6 Salmonella) and negative results
- Systematic sampling: random, risk-based, and intensified programs
- Product categories, facility data, genetic fingerprints

**Strengths:**
- ✅ **Statistical power**: 27,211 samples with both positives AND negatives
- ✅ **Systematic sampling**: Random + risk-based = less selection bias
- ✅ **Proactive surveillance**: Catches contamination before consumer exposure
- ✅ **Product categories**: 110 unique product types with contamination rates
- ✅ **Denominator data**: Can calculate true rates (positives/total tests)
- ✅ **Environmental context**: Facility contamination vs product contamination
- ✅ **Genetic data**: Track strain persistence and cross-contamination
- ✅ **Temporal granularity**: Daily collection dates for trend analysis

**Weaknesses:**
- ❌ **Not consumer-facing**: Most samples never reached market
- ❌ **Generic product names**: "RTE-Fully Cooked, Sausage Products-Pork" not brand-specific
- ❌ **State-level only**: No city-level geographic detail
- ❌ **Missing "popularity" metric**: No sales, consumption, or market share data
- ❌ **Single year**: FY2025 only - cannot show temporal "increase"
- ❌ **No distribution data**: Don't know where products would have been sold

**Data Available:**
- Sample source/product type
- Test results (positive/negative)
- Establishment location (state)
- Collection date
- Pathogen genetic fingerprints
- Facility repeat offenders

---

## Critical Missing Component: "Popularity" Data

**Neither dataset includes food popularity metrics needed to test your hypothesis directly.**

To truly test if popular foods have higher contamination, you need:
- **Sales volume**: Units sold, revenue by product category
- **Consumption patterns**: USDA food availability data, dietary surveys
- **Market share**: Top brands, restaurant sales data
- **Consumer trends**: Plant-based alternatives, organic products, etc.

**Potential external data sources:**
1. **USDA Economic Research Service (ERS)**
   - Per capita consumption by meat type
   - Food availability data system
   - Example: Americans consume ~60 lbs chicken/year, ~56 lbs beef/year

2. **Nielsen/IRI Retail Sales Data** (commercial)
   - Brand-level sales volumes
   - Product category growth rates

3. **CDC FoodNet Population Survey**
   - Food consumption frequency
   - High-risk food exposure

4. **USDA Census of Agriculture**
   - Production volumes by commodity
   - Slaughter statistics

---

## Testing the Hypothesis: Which Dataset is Better?

### Scenario A: "Are popular food types more contaminated?"

**Lab Sampling Data is Superior** ✅

**Why:**
- Can calculate contamination **rates** by product category (e.g., chicken vs beef vs pork)
- Denominator data exists (total samples tested per product)
- Can stratify by product type: "RTE chicken" vs "RTE pork" vs "RTE beef"

**Analysis approach:**
```
1. Group samples by product category
2. Calculate contamination rate: Positives/Total tests
3. Merge with USDA consumption data (external)
4. Test correlation: Do high-consumption foods have higher contamination?
```

**Example from current data:**
| Product Type | Samples | Positives | Rate | Annual US Consumption* |
|--------------|---------|-----------|------|------------------------|
| RTE Chicken | 1,208 | 3 | 0.25% | 60 lbs/person |
| RTE Pork Sausage | 952 | 8 | 0.84% | 25 lbs/person |
| RTE Beef | 498 | 2 | 0.40% | 56 lbs/person |

*Would need to add external data

**Statistical test:** Correlation coefficient between consumption volume and contamination rate

---

### Scenario B: "Is there an increase in recalls for popular foods?"

**Recall Data is Better** ✅ (but needs multi-year dataset)

**Why:**
- Recall data shows actual consumer impact
- Brand names allow matching to sales data
- Volume recalled = proxy for market size
- Class I recalls indicate high-risk popular products

**Analysis approach:**
```
1. Collect 5-10 years of recall data
2. Categorize by product type
3. Merge with sales/consumption trends
4. Time series analysis: Are recalls increasing for high-consumption foods?
```

**Challenge:** Current example is single recall (003-2026). Need historical dataset.

---

### Scenario C: "Do popular products have higher contamination at production?"

**Lab Sampling Data is Superior** ✅

**Why:**
- Shows contamination at source (production facilities)
- Environmental swabs show facility-level problems
- Can identify if popular product facilities are under-resourced
- Larger sample size for statistical significance

**Analysis approach:**
```
1. Identify establishments producing high-volume products
2. Compare contamination rates: high-volume vs low-volume facilities
3. Control for facility size, production complexity
4. Test: Do popular product producers have higher environmental contamination?
```

---

## Recommended Combined Analysis Strategy

**Best approach: Integrate both datasets for comprehensive evidence**

### Step 1: Lab Data - Systematic Surveillance Baseline
**Purpose:** Establish contamination rates by product category

**Analysis:**
1. Calculate contamination rate by product type (current data: 0.77% Listeria overall)
2. Identify high-risk product categories
   - Current data shows: Non-contact surfaces (3.54%), Pork sausage (0.84%), Diced chicken (1.81%)
3. Map product categories to USDA consumption data
4. Test correlation: Consumption volume vs contamination rate

**Deliverable:** "Product contamination risk matrix" showing which popular foods are most contaminated at production

---

### Step 2: Recall Data - Consumer Impact Assessment
**Purpose:** Show which contaminated products reached consumers

**Analysis:**
1. Scrape/collect USDA FSIS recalls (last 5 years recommended)
2. Categorize recalls by product type
3. Calculate recall frequency and volume by category
4. Cross-reference with lab sampling data: Do lab positives predict recalls?

**Deliverable:** "Popular products recall dashboard" showing temporal trends

---

### Step 3: Integration - The Compelling Story
**Purpose:** Connect production contamination to consumer risk

**Key Questions Answered:**
1. ✅ Are chicken products (most consumed) also most contaminated? (Lab data)
2. ✅ Are chicken recalls increasing? (Recall data + time series)
3. ✅ Do facilities producing popular products have more environmental contamination? (Lab data)
4. ✅ Which popular products pose the greatest consumer risk? (Combined)

**Visualization:**
```
Interactive Dashboard with:
- State map: Contamination detections (lab data) + Recall distribution (recall data)
- Time series: Lab positives vs recalls over time
- Product matrix: Consumption volume vs contamination rate vs recall frequency
- Facility risk score: Popular product producers with repeat contamination
```

---

## Evidence Quality Assessment

### Testing: "Popular foods have higher contamination"

| Dataset | Sample Size | Statistical Power | Causation | Consumer Impact | Verdict |
|---------|-------------|-------------------|-----------|-----------------|---------|
| **Lab Sampling** | 27,211 | ✅ High | ⚠️ Correlation only | ❌ Pre-market | **Better** |
| **Recall Data** | ~50-200/year | ❌ Low | ⚠️ Correlation only | ✅ Direct | Supplemental |

**Winner:** Lab sampling data (with external consumption data)

---

### Testing: "Recalls are increasing for popular foods"

| Dataset | Temporal Depth | Trend Detection | Severity | Product Names | Verdict |
|---------|---------------|-----------------|----------|---------------|---------|
| **Lab Sampling** | 1 year (FY2025) | ❌ Insufficient | N/A | Generic | Insufficient |
| **Recall Data** | Multi-year | ✅ Good | ✅ Class I/II/III | ✅ Brands | **Better** |

**Winner:** Recall data (needs multi-year collection)

---

## Addressing Confounding Factors

**Critical:** Correlation ≠ causation. Consider confounders:

### Confounder 1: Sampling Intensity
- **Problem:** Popular products may be tested more frequently (risk-based sampling)
- **Control:** Calculate detection rate per sample, not absolute positives
- **Data needed:** Project code (RTEPROD_RISK vs RTEPROD_RAND)

### Confounder 2: Production Volume
- **Problem:** More production = more opportunity for contamination
- **Control:** Normalize by production volume (lbs produced)
- **Data needed:** USDA production statistics (external)

### Confounder 3: Facility Complexity
- **Problem:** Popular products from larger, more complex facilities
- **Control:** Stratify by facility size/type
- **Data needed:** Establishment production volume (not in current data)

### Confounder 4: Detection Technology
- **Problem:** Better detection methods find more contamination
- **Control:** Time series with consistent methodology
- **Data needed:** Lab method changes (in metadata)

---

## Data Gaps & Recommendations

### Critical Gaps:
1. ❌ **No popularity metric** in either dataset
   - **Solution:** Merge with USDA ERS consumption data

2. ❌ **Single year of lab data** (FY2025 only)
   - **Solution:** Obtain FY2014-2024 historical data (available from USDA)

3. ❌ **Single recall example** (not full dataset)
   - **Solution:** Scrape USDA FSIS recall website or use FSIS API

4. ❌ **No production volume** data
   - **Solution:** Request from FSIS or use USDA slaughter statistics

5. ❌ **No brand/market data** in lab sampling
   - **Solution:** Cannot fix - data is anonymized for facility privacy

---

## Actionable Next Steps

### Phase 1: Enhance Current Lab Data Analysis ⭐ **START HERE**

**Why:** You already have this data with 27,211 samples

**Tasks:**
1. ✅ Categorize sample sources into product types (chicken, beef, pork, etc.)
2. ✅ Calculate contamination rates by category
3. 🔄 Merge with USDA per-capita consumption data
4. 🔄 Create "Contamination Risk by Product Popularity" matrix
5. 🔄 Geographic analysis: Do high-consumption states have more contamination?

**Time estimate:** Medium complexity analysis

**Deliverable:** "Popular Foods Contamination Analysis" report + interactive dashboard

---

### Phase 2: Collect Multi-Year Recall Data

**Why:** Test temporal "increase" claim

**Tasks:**
1. 🔄 Scrape USDA FSIS recall announcements (2020-2026)
2. 🔄 Structure data: date, product, pathogen, volume, states
3. 🔄 Categorize recalls by product type
4. 🔄 Time series analysis: Recall frequency trends
5. 🔄 Cross-reference with consumption trends

**Data source:** https://www.fsis.usda.gov/recalls

**Deliverable:** "Recall Trends Dashboard" with temporal analysis

---

### Phase 3: Integrated Analysis

**Why:** Most compelling evidence combines both

**Tasks:**
1. 🔄 Merge lab contamination rates with recall frequencies
2. 🔄 Create unified product risk score: (Contamination rate × Recall frequency × Consumption volume)
3. 🔄 Interactive map: Lab positives + Recall distribution by state
4. 🔄 Predictive model: Can lab data predict future recalls?

**Deliverable:** "Comprehensive Food Safety Risk Dashboard"

---

## Conclusion: Which Dataset is Better?

### For Your Specific Hypothesis:

**"Is there an increase in contamination/recalls traced to popular foods?"**

**Answer:**
1. **Lab Sampling Data (current)** is better for testing **contamination rates** by product type
2. **Recall Data (need to collect)** is better for testing **temporal increases**
3. **Both combined** is optimal for a compelling, comprehensive analysis

### Immediate Recommendation:

**Start with Phase 1: Lab Data Analysis** ⭐

**Why:**
- You have 27,211 samples ready to analyze
- Can calculate contamination rates by product immediately
- Only need to merge with free USDA consumption data
- Provides statistical foundation for later recall analysis

**Key Insight from Current Data:**
```
Non-contact surface sponges: 3.54% contamination rate (92/2600)
RTE Pork sausage: 0.84% contamination rate (8/952)
RTE Diced chicken: 1.81% contamination rate (8/441)
```

These are testable right now - just need to add "popularity" context via external consumption data.

---

## Visualization Proposal: Interactive Contamination Map

Based on lab sampling data, create:

### Map View:
- **Choropleth by state**: Contamination detection rate
- **Tooltips**: Top contaminated products per state
- **Filters**: Product type, pathogen, date range

### Product Risk Dashboard:
- **Scatter plot**: Consumption volume (x-axis) vs Contamination rate (y-axis)
- **Bubble size**: Number of samples
- **Color**: Product category (chicken, beef, pork, etc.)

### Timeline View:
- **Line chart**: Monthly contamination rate by product type
- **Annotations**: Major recalls (once recall data collected)

**Would you like me to create a detailed implementation plan for this dashboard?**
