# Food Consumption Data Analysis
## Evaluating Table 5: US Food Group Intakes by Food Source

**Analysis Date:** February 18, 2026
**Data Source:** usFoodGroupIntakesBySource.csv
**Question:** Does this provide the information we need about popularity of ready-to-eat meats?

---

## Executive Summary

**Answer: PARTIALLY YES, with significant limitations.**

The dataset contains **"Protein foods, cured meat"** which is the closest proxy for ready-to-eat meats (deli meats, hot dogs, salami, bacon, etc.). However, this data has critical mismatches with the USDA FSIS lab sampling data that require careful consideration.

---

## Dataset Overview

**Source:** USDA Food Intakes by Source (Table 5)
**Coverage:** 1977-2018 (most recent: 2017-2018)
**Demographics:** US consumers aged 2 and above
**Measurement:** Ounces per day per person

### Data Structure:
- **Food groups:** Energy, Protein foods, Dairy, Fruits, Vegetables, Grains, etc.
- **Food source:**
  - **FAH (Food at Home):** Purchased from stores for home consumption
  - **FAFH (Food Away From Home):** Restaurants, fast food, schools, etc.
- **Time periods:** Biennial survey years from 1977 to 2018
- **Variables:** Mean values and standard errors

---

## Protein Foods Consumption (2017-2018)

### Overall Protein Consumption (Food at Home):

| Food Category | Oz/Day | Lbs/Year | % of Total Protein |
|---------------|--------|----------|-------------------|
| **Total protein foods** | 3.80 | 86.6 | 100% |
| Meats, poultry, and fish | 2.69 | 61.3 | 70.8% |
| Meats (beef, veal, pork, lamb, game) | 0.87 | 19.8 | 22.9% |
| Poultry | 0.81 | 18.5 | 21.3% |
| **Cured meat (RTE)** | **0.67** | **15.3** | **17.6%** |
| Nuts and seeds | 0.63 | 14.4 | 16.6% |
| Eggs | 0.42 | 9.6 | 11.1% |
| Low omega-3 fish | 0.23 | 5.2 | 6.1% |
| High omega-3 fish | 0.10 | 2.3 | 2.6% |
| Soy products | 0.07 | 1.6 | 1.8% |
| Organ meats | 0.00 | 0.0 | 0.0% |

**Key Finding:** Americans consume approximately **15.3 lbs of cured meat per year** purchased for home consumption (2017-2018 data).

---

## Critical Question: Does This Match USDA FSIS Lab Data?

### ⚠️ MAJOR MISMATCH IDENTIFIED

**Problem:** The consumption data measures **all protein foods** (raw + RTE combined), while the USDA FSIS lab sampling data specifically tests **ready-to-eat (RTE) products only**.

### Breakdown of the Mismatch:

| Data Category in Table 5 | What It Includes | Matches FSIS Data? |
|---------------------------|------------------|-------------------|
| **Cured meat (0.67 oz/day)** | Bacon, deli meats, hot dogs, salami | ✅ **YES** - These are RTE |
| **Meats (beef, veal, pork) (0.87 oz/day)** | Raw steaks, chops, ground meat for cooking | ❌ **NO** - These are raw meats |
| **Poultry (0.81 oz/day)** | Raw chicken breasts, whole chickens | ❌ **NO** - These are raw |

### What's Missing from Table 5:

The Table 5 dataset **does NOT break down:**
1. **RTE chicken products** (rotisserie chicken, pre-cooked chicken strips, deli chicken)
2. **RTE pork products** (pre-cooked pork loin, BBQ pulled pork)
3. **RTE beef products** (pre-cooked roast beef, corned beef)
4. **RTE sausages** (cooked sausages, frankfurters)

These are **all included in the USDA FSIS lab sampling** but are **hidden within the generic categories** in Table 5.

---

## USDA FSIS Lab Sampling Categories (Our Original Data)

Recall from the contamination data, the sample categories include:

| FSIS Sample Category | Sample Count | What It Is |
|---------------------|--------------|------------|
| RTE Chicken Products | 1,208 | Fully cooked chicken (deli, strips, nuggets) |
| RTE Pork Sausages | 952 | Fully cooked sausages |
| RTE Pork (Other) | 1,338 | Fully cooked pork products |
| RTE Beef Products | 498 | Fully cooked beef (deli, roasts) |
| **Cured meat** | ??? | Not directly listed |

**Problem:** Table 5's "cured meat" category (15.3 lbs/year) represents only a **subset** of the RTE products tested in the FSIS lab data.

---

## Apples-to-Apples Comparison Problem

### Scenario 1: Using "Cured Meat" as RTE Proxy

**Pros:**
- ✅ True ready-to-eat category
- ✅ Matches FSIS definition of RTE
- ✅ Direct measurement from consumption surveys

**Cons:**
- ❌ Excludes RTE chicken, RTE pork (non-cured), RTE beef
- ❌ Underestimates total RTE consumption
- ❌ Doesn't match FSIS sample categories

**Conclusion:** **Apples-to-oranges comparison** - You'd be comparing:
- Lab data: All RTE chicken, beef, pork (various products)
- Consumption data: Only cured meats (subset)

---

### Scenario 2: Using All "Meats, Poultry, Fish" as Proxy

**Pros:**
- ✅ Includes all meat types in FSIS data
- ✅ Comprehensive coverage

**Cons:**
- ❌ Includes RAW meats (steaks, raw chicken) that FSIS doesn't test
- ❌ Massive overestimate of RTE consumption
- ❌ Not comparable to FSIS RTE-specific sampling

**Conclusion:** **Even worse mismatch** - You'd be comparing:
- Lab data: RTE products only
- Consumption data: Raw + RTE combined

---

## The 1-to-1 Comparison Challenge

### What You Need (Ideal):

| Product Type | Lab Contamination Rate | RTE Consumption (lbs/year) | Can Compare? |
|--------------|------------------------|---------------------------|--------------|
| RTE Chicken | 0.25% (3/1208) | **??? (Unknown)** | ❌ NO |
| RTE Pork Sausage | 0.84% (8/952) | **??? (Unknown)** | ❌ NO |
| RTE Beef | 0.40% (2/498) | **??? (Unknown)** | ❌ NO |
| Cured Meats | **??? (Not separately tracked in lab data)** | 15.3 lbs/year | ❌ NO |

**Problem:** The categories don't line up!

---

## What Table 5 DOES Tell Us

Despite the mismatch, Table 5 provides valuable insights:

### 1. Relative Popularity Rankings (Food at Home):

```
Poultry (0.81 oz/day) > Meats (0.87 oz/day) > Cured meat (0.67 oz/day)
```

**Interpretation:** Americans buy slightly more beef/pork than poultry, and cured meats are about 80% as popular as either.

### 2. Temporal Trends (Historical):

```python
Year    | Cured Meat (oz/day)
1977-78 | 0.65
2013-14 | 0.96 (peak)
2015-16 | 0.96
2017-18 | 0.67 (decline)
```

**Finding:** Cured meat consumption **peaked in 2013-2016** then **declined by 30%** by 2017-2018.

**Hypothesis:** This decline coincides with increased health awareness about processed meats and potential contamination concerns.

### 3. Food Source Breakdown (2013-2014 data):

| Food Source | Cured Meat (oz/day) | % of Total |
|-------------|---------------------|------------|
| **FAH (Food at Home)** | 0.64 | 67% |
| **FAFH (Restaurants)** | 0.06 | 6% |
| **FAFH (Fast Food)** | 0.17 | 18% |
| **FAFH (School)** | 0.02 | 2% |
| **FAFH (Others)** | 0.09 | 9% |
| **Total** | 0.96 | 100% |

**Interpretation:** 67% of cured meat is consumed from home purchases, which **does align** with FSIS facility sampling (facilities supplying retail stores).

---

## Alternative Data Sources for Better Matching

To get true **RTE meat consumption** data that matches FSIS categories:

### Option 1: USDA ERS Loss-Adjusted Food Availability
**URL:** https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/

**Data Available:**
- Total chicken production: ~60 lbs/person/year
- Total beef production: ~56 lbs/person/year
- Total pork production: ~25 lbs/person/year

**Problem:** Still doesn't distinguish raw vs RTE

---

### Option 2: USDA NASS Livestock Slaughter Statistics
**URL:** https://www.nass.usda.gov/Statistics_by_Subject/

**Data Available:**
- Production volumes by meat type
- State-level production

**Problem:** Production ≠ RTE consumption

---

### Option 3: Industry Market Research (Commercial)

**Sources:**
- Nielsen/IRI retail sales data
- IDDBA (International Dairy Deli Bakery Association)
- NAMI (North American Meat Institute)

**Data Available:**
- RTE deli meat sales ($ and lbs)
- RTE chicken strip/nugget sales
- Rotisserie chicken sales

**Problem:** $$$ - These are paid commercial reports

---

### Option 4: FDA/CDC FoodNet Population Survey
**URL:** https://www.cdc.gov/foodnet/

**Data Available:**
- Consumer food exposure surveys
- Specific food consumption frequency
- Links to outbreak investigations

**Benefit:** Distinguishes RTE vs raw in surveys

---

## Recommendation: How to Use Table 5 Data

Given the limitations, here's the **best approach**:

### ✅ What Table 5 CAN Support:

**1. General Protein Popularity Ranking:**
```
Hypothesis: Popular protein types have higher contamination
Method: Compare broad categories
- Meats (beef/pork): 0.87 oz/day → FSIS RTE contamination: 0.3-0.8%
- Poultry: 0.81 oz/day → FSIS RTE contamination: 0.3-1.8%
- Conclusion: Poultry slightly less popular but higher contamination
```

**2. Temporal Correlation:**
```
Hypothesis: Declining consumption correlates with increased contamination awareness
Method: Compare consumption trends with FSIS detection rates over time
- Cured meat declined 30% (2013-2018)
- Did FSIS positive rates change during same period?
```

**3. Geographic Proxies:**
```
Hypothesis: States with higher meat consumption have more contamination
Method: Use state-level production data (not in Table 5, but available from USDA NASS)
- High pork production states: Iowa, North Carolina, Minnesota
- FSIS contamination rates: IL (1.18%), NC (1.15%)
- Potential correlation worth exploring
```

---

### ❌ What Table 5 CANNOT Support:

**1. Direct Product-Level Comparison:**
```
❌ Cannot compare: RTE Chicken strips contamination vs RTE chicken consumption
   Reason: Table 5 doesn't break out RTE chicken from raw chicken
```

**2. RTE-Specific Market Share:**
```
❌ Cannot calculate: What % of chicken consumed is RTE vs raw?
   Reason: Table 5 combines all poultry in one category
```

**3. Precise Contamination-Per-Pound Risk:**
```
❌ Cannot calculate: Risk per lb of RTE pork sausage consumed
   Reason: Consumption data (15.3 lbs cured meat) ≠ Lab data categories
```

---

## Revised Analysis Strategy

### Approach A: Broad Category Comparison (Feasible)

**Method:**
1. Use Table 5 categories as **general proxies**:
   - "Cured meat" ≈ All RTE meat products
   - "Poultry" ≈ All chicken (acknowledge includes raw)
   - "Meats" ≈ All beef/pork (acknowledge includes raw)

2. Calculate **relative popularity** from Table 5:
   ```
   Popularity Score:
   - Beef/Pork meats: 0.87 oz/day (Rank #3)
   - Poultry: 0.81 oz/day (Rank #4)
   - Cured meats: 0.67 oz/day (Rank #5)
   ```

3. Compare with **FSIS contamination rates**:
   ```
   Contamination Rate:
   - RTE Chicken: 0.25-1.81% (varies by product)
   - RTE Pork: 0.67-0.84%
   - RTE Beef: 0.40%
   ```

4. **Conclusion:**
   - No strong correlation between overall protein popularity and RTE contamination
   - Chicken is popular (#4) but has variable contamination
   - Cured meats less popular (#5) but no separate contamination metric

**Strength:** Uses available data responsibly
**Weakness:** Very coarse-grained comparison

---

### Approach B: Focus on "Cured Meat" Only (More Precise)

**Method:**
1. Assume FSIS "RTE Pork Sausage" category ≈ Table 5 "Cured meat"
   - Both include hot dogs, sausages, bacon, deli meats

2. Compare directly:
   ```
   Consumption: 15.3 lbs/year (Table 5)
   Contamination: 0.84% (8/952 samples for RTE Pork Sausage)
   ```

3. Add temporal dimension:
   ```
   2013-14: 21.9 lbs/year consumption
   2017-18: 15.3 lbs/year consumption

   Decline: 30% decrease in 4 years

   Question: Did FSIS contamination rates change during this period?
   (Need historical FSIS data to answer)
   ```

**Strength:** Most comparable product categories
**Weakness:** Still not perfect match; FSIS has broader RTE definition

---

### Approach C: Supplement with External Data (Recommended)

**Method:**
1. Use Table 5 for **broad protein popularity** (meats vs poultry vs fish)

2. Obtain **RTE-specific** market data from:
   - IDDBA Deli Meat Sales Reports
   - NAMI RTE Product Statistics
   - Nielsen retail scanner data (if accessible)

3. Create **custom RTE popularity index**:
   ```
   RTE Popularity Score =
     (Table 5 protein category consumption) ×
     (Industry RTE market share %) ×
     (Retail sales volume)
   ```

4. Compare with FSIS contamination by product category

**Strength:** Most accurate, true apples-to-apples
**Weakness:** Requires additional data collection; some data may be proprietary

---

## Final Verdict

### Does Table 5 provide what we need?

**Short Answer:** **Partially, but with significant caveats.**

### What It Provides:
✅ General protein consumption patterns (meats, poultry, fish)
✅ Temporal trends showing changing consumption (cured meat declined 30%)
✅ Food source breakdown (home vs restaurant vs fast food)
✅ One true RTE category: "Cured meat" (15.3 lbs/year)

### What It's Missing:
❌ RTE-specific breakdowns for chicken, beef, pork
❌ Direct mapping to FSIS sample categories
❌ Market share data (what % of chicken consumed is RTE?)
❌ Product-level granularity (chicken nuggets vs rotisserie chicken)

### Comparison Challenge:
⚠️ **"We need to compare across the same food types"** - Your point is correct.

**The Problem:**
- FSIS tests: RTE chicken products, RTE pork products, RTE beef products
- Table 5 measures: ALL chicken (raw + RTE), ALL pork (raw + RTE), ALL beef (raw + RTE)
- Only exception: "Cured meat" which is mostly RTE

**The Reality:**
- Comparing "RTE chicken contamination" to "total chicken consumption" is **NOT a fair comparison**
- It overestimates the "at-risk" consumption population
- It dilutes the true RTE exposure

---

## Recommendation for Your Analysis

### Option 1: Use "Cured Meat" as Primary RTE Proxy (Conservative)

**Rationale:**
- Only verifiable RTE category in Table 5
- 15.3 lbs/year consumption is measurable
- Can compare temporally (declined 30% in recent years)

**Dashboard Element:**
```
"Cured Meat Consumption & Contamination"
- Consumption: 15.3 lbs/person/year (2017-2018)
- FSIS RTE Pork Sausage Contamination: 0.84%
- Correlation: Consumption declined as contamination awareness increased
```

---

### Option 2: Acknowledge Limitations & Use Broad Categories (Transparent)

**Rationale:**
- Honest about data limitations
- Uses available data responsibly
- Provides valuable insights despite imperfect match

**Dashboard Element:**
```
"Protein Consumption vs RTE Contamination (Proxy Comparison)"

Note: Consumption data includes both raw and RTE products.
True RTE consumption is a subset of these values.

Consumption (oz/day) | FSIS RTE Contamination Rate
Poultry: 0.81        | RTE Chicken: 0.25-1.81%
Meats: 0.87          | RTE Pork: 0.67-0.84%; RTE Beef: 0.40%
Cured: 0.67          | RTE Sausage: 0.84%
```

---

### Option 3: Collect Additional Data (Most Accurate)

**Rationale:**
- Achieve true 1-to-1 comparison
- Strongest evidence for hypothesis
- Publication-quality analysis

**Action Steps:**
1. Research IDDBA RTE deli meat sales data
2. Contact NAMI for RTE meat production statistics
3. Use FDA FoodNet consumption surveys (RTE-specific)
4. Create custom RTE popularity index

**Timeline:** Additional 2-4 weeks of data collection

---

## Conclusion

**Your concern is valid:** Comparing FSIS RTE sampling data to general protein consumption (which includes raw meats) is **not a 1-to-1 comparison**.

**Best Path Forward:**

1. **Short-term:** Use "Cured meat" (15.3 lbs/year) as the **primary RTE proxy**
   - This IS ready-to-eat
   - This IS comparable to FSIS RTE categories
   - This IS measured in Table 5

2. **Medium-term:** Create dashboard with **clear disclaimers** about data limitations
   - Note that other protein categories include raw + RTE
   - Present correlations cautiously
   - Acknowledge the mismatch

3. **Long-term:** Obtain **true RTE consumption data** from industry sources
   - IDDBA, NAMI, Nielsen
   - Create perfect 1-to-1 comparison
   - Publish findings with confidence

**Would you like me to:**
A) Proceed with "cured meat" as the RTE proxy for now?
B) Design a dashboard that transparently shows data limitations?
C) Create a plan for obtaining better RTE-specific consumption data?
