# Jupyter Notebook Visualization Plan: Consumption + Contamination Integration

**Created:** February 18, 2026
**Purpose:** Pseudocode plan for creating visualizations that combine consumption data with contamination data

---

## Clarification: What Data Goes Where?

### Original 3-Map-Implementation-Plan.md Strategy:

The plan was designed to use **BOTH datasets combined**:

| Visualization | Primary Data | Secondary Data | Purpose |
|--------------|--------------|----------------|---------|
| **State Choropleth Map** | Contamination data | None | Show contamination rates by state |
| **Product Risk Dashboard** | Contamination data | **Consumption data** | Test if popular foods have higher contamination |
| **Timeline Analysis** | Contamination data | **Consumption data (optional)** | Show trends over time with consumption overlay |
| **Consumption Trend Chart** | **Consumption data** | Contamination data (optional) | Show how consumption changed 2009-2018 |

---

## Data Integration Strategy

### Dataset 1: USDA FSIS Lab Sampling (Contamination)
- **What:** 27,211 samples from 2,364 facilities
- **When:** FY2025 (Oct 2024 - Sep 2025)
- **Granularity:** Sample-level (daily collection dates, facility-specific)
- **Key fields:**
  - `establishment_state` - State location
  - `sample_source_name` - Product type (RTE Chicken, RTE Pork Sausage, etc.)
  - `lm_listeria_analysis` - Positive/Negative
  - `collection_date` - Sample date

### Dataset 2: USDA Food Consumption (Table 5)
- **What:** Per-capita consumption of protein foods
- **When:** 1977-2018 (most recent: 2017-2018)
- **Granularity:** National averages, biennial survey years
- **Key fields:**
  - `Food group` - Protein category (Cured meat, Poultry, Meats, etc.)
  - `Survey years:Variable` - Time period
  - `Value` - Oz per day per person
  - `Food source` - FAH (Food at Home) vs FAFH

### Integration Approach:

```
CONTAMINATION DATA (27K samples, FY2025)
    ↓
Aggregate by product category
    ↓
Calculate contamination rates
    ↓
Match to consumption categories ← CONSUMPTION DATA (2017-2018)
    ↓
Combined analysis: Do popular foods have higher contamination?
```

**Challenge:**
- Contamination: FY2025
- Consumption: 2017-2018
- **7-year gap** - must acknowledge in visualizations

---

## Notebook Structure Plan

### Proposed Notebooks:

```
listeria-tracker/
├── visualization_4_product_analysis.ipynb (EXISTING)
├── dashboard_6_program_effectiveness.ipynb (EXISTING)
├── visualization_7_consumption_trends.ipynb (NEW) ← Consumption over time
├── visualization_8_consumption_vs_contamination.ipynb (NEW) ← Combined analysis
└── visualization_9_state_map_choropleth.ipynb (NEW) ← Interactive map
```

---

## Notebook 1: visualization_7_consumption_trends.ipynb

**Purpose:** Visualize consumption trends 1977-2018 from Table 5 data

**Outputs:**
1. Line chart: Cured meat consumption over time
2. Bar chart: Protein category comparison (2017-2018)
3. Heatmap: Consumption by category and year
4. Key findings summary

### Pseudocode:

```python
# ============================================================================
# NOTEBOOK: visualization_7_consumption_trends.ipynb
# PURPOSE: Analyze and visualize USDA consumption data (Table 5)
# ============================================================================

# --- SECTION 1: SETUP ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# --- SECTION 2: LOAD CONSUMPTION DATA ---

def load_consumption_data(csv_path):
    """
    Load Table 5 consumption data

    Returns:
        df: Full dataset
        protein_df: Filtered to protein foods only
    """
    # Load CSV
    df = pd.read_csv(csv_path)

    # Filter for protein foods
    protein_df = df[df['Food group'].str.contains('Protein foods', case=False, na=False)]

    # Filter for Food at Home (FAH) only - closest to RTE retail
    protein_df = protein_df[protein_df['Food source'] == 'FAH']

    # Filter for US average (not demographic subgroups)
    protein_df = protein_df[protein_df['Demographics'] == 'US consumers aged 2 and above']

    # Filter for Mean values (not SE)
    protein_df = protein_df[protein_df['Survey years:Variable'].str.contains('Mean', na=False)]

    return df, protein_df

# Load data
df_full, df_protein = load_consumption_data('usFoodGroupIntakesBySource.csv')

print(f"Total records: {len(df_full)}")
print(f"Protein food records: {len(df_protein)}")
print(f"Unique protein categories: {df_protein['Food group'].nunique()}")

# --- SECTION 3: DATA CLEANING ---

def clean_consumption_data(df):
    """
    Clean and transform consumption data

    Returns:
        clean_df: Cleaned dataframe with parsed years and numeric values
    """
    df_clean = df.copy()

    # Extract year from 'Survey years:Variable' (e.g., "2017-2018-Mean" -> "2017-2018")
    df_clean['year_range'] = df_clean['Survey years:Variable'].str.replace('-Mean', '')

    # Create midpoint year for plotting (e.g., "2017-2018" -> 2017.5)
    def parse_year(year_str):
        if '-' in year_str:
            years = year_str.split('-')
            start_year = int(years[0])
            return start_year  # Use start year for simplicity
        return None

    df_clean['year'] = df_clean['year_range'].apply(parse_year)

    # Ensure Value is numeric
    df_clean['value_oz_per_day'] = pd.to_numeric(df_clean['Value'], errors='coerce')

    # Calculate lbs per year
    df_clean['value_lbs_per_year'] = df_clean['value_oz_per_day'] * 365 / 16

    # Remove rows with missing values
    df_clean = df_clean.dropna(subset=['year', 'value_oz_per_day'])

    return df_clean

df_protein_clean = clean_consumption_data(df_protein)

# Preview
print("\nCleaned data sample:")
print(df_protein_clean[['Food group', 'year', 'value_oz_per_day', 'value_lbs_per_year']].head(10))

# --- SECTION 4: VISUALIZATION 1 - CURED MEAT OVER TIME ---

def plot_cured_meat_trend(df):
    """
    Line chart showing cured meat consumption 1977-2018
    """
    # Filter for cured meat only
    cured = df[df['Food group'] == 'Protein foods, cured meat'].copy()
    cured = cured.sort_values('year')

    # Create figure
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Plot oz/day
    ax1.plot(cured['year'], cured['value_oz_per_day'],
             marker='o', linewidth=2, markersize=8, color='#d62728', label='Oz/Day')
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Ounces per Day', fontsize=12, color='#d62728')
    ax1.tick_params(axis='y', labelcolor='#d62728')
    ax1.grid(True, alpha=0.3)

    # Add lbs/year on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(cured['year'], cured['value_lbs_per_year'],
             marker='s', linewidth=2, markersize=8, color='#1f77b4',
             linestyle='--', label='Lbs/Year')
    ax2.set_ylabel('Pounds per Year', fontsize=12, color='#1f77b4')
    ax2.tick_params(axis='y', labelcolor='#1f77b4')

    # Highlight peak
    peak_idx = cured['value_oz_per_day'].idxmax()
    peak_year = cured.loc[peak_idx, 'year']
    peak_value = cured.loc[peak_idx, 'value_oz_per_day']
    ax1.annotate(f'PEAK: {peak_value:.2f} oz/day\n({peak_year})',
                 xy=(peak_year, peak_value),
                 xytext=(peak_year - 5, peak_value + 0.05),
                 arrowprops=dict(arrowstyle='->', color='red', lw=2),
                 fontsize=11, fontweight='bold', color='red')

    # Highlight 2011 (major outbreak year)
    if 2011 in cured['year'].values:
        ax1.axvline(x=2011, color='orange', linestyle=':', linewidth=2, alpha=0.7)
        ax1.text(2011, ax1.get_ylim()[1] * 0.95, '2011\nMajor Outbreaks',
                 ha='center', fontsize=10, color='orange', fontweight='bold')

    # Highlight 2015 (WHO warning)
    if 2015 in cured['year'].values:
        ax1.axvline(x=2015, color='purple', linestyle=':', linewidth=2, alpha=0.7)
        ax1.text(2015, ax1.get_ylim()[1] * 0.85, '2015\nWHO Warning',
                 ha='center', fontsize=10, color='purple', fontweight='bold')

    # Title
    plt.title('Cured Meat (RTE) Consumption Trends: 1977-2018\nDeclining Consumption After 2009 Peak',
              fontsize=14, fontweight='bold', pad=20)

    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

    plt.tight_layout()
    plt.show()

    return cured

cured_meat_trend = plot_cured_meat_trend(df_protein_clean)

# Calculate key statistics
peak_year = cured_meat_trend.loc[cured_meat_trend['value_oz_per_day'].idxmax(), 'year']
peak_value = cured_meat_trend['value_oz_per_day'].max()
recent_value = cured_meat_trend[cured_meat_trend['year'] == 2017]['value_oz_per_day'].values[0]
decline_pct = ((recent_value - peak_value) / peak_value) * 100

print(f"\nKEY FINDINGS:")
print(f"  Peak: {peak_year} at {peak_value:.2f} oz/day ({peak_value * 365 / 16:.1f} lbs/year)")
print(f"  Recent: 2017 at {recent_value:.2f} oz/day ({recent_value * 365 / 16:.1f} lbs/year)")
print(f"  Decline: {decline_pct:.1f}% from peak to recent")

# --- SECTION 5: VISUALIZATION 2 - PROTEIN CATEGORY COMPARISON ---

def plot_protein_categories_2017(df):
    """
    Bar chart comparing protein categories in 2017-2018
    """
    # Filter for 2017 data
    df_2017 = df[df['year'] == 2017].copy()

    # Get unique food groups and their values
    categories = df_2017.groupby('Food group')['value_oz_per_day'].first().reset_index()
    categories = categories.sort_values('value_oz_per_day', ascending=True)

    # Only keep main categories (exclude sub-subcategories)
    main_cats = [
        'Protein foods, total',
        'Protein foods, meats, poultry, and fish',
        'Protein foods, meats (beef, veal, pork, lamb, game)',
        'Protein foods, poultry',
        'Protein foods, cured meat',
        'Protein foods, nuts and seeds',
        'Protein foods, eggs',
        'Protein foods, low Omega-3 fatty fish',
        'Protein foods, high Omega-3 fatty fish',
        'Protein foods, soy products',
        'Protein foods, organ meats'
    ]
    categories = categories[categories['Food group'].isin(main_cats)]

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, 8))

    bars = ax.barh(categories['Food group'], categories['value_oz_per_day'],
                    color='#2ca02c', alpha=0.7, edgecolor='black', linewidth=1.5)

    # Highlight cured meat
    cured_idx = categories[categories['Food group'] == 'Protein foods, cured meat'].index[0]
    cured_pos = list(categories.index).index(cured_idx)
    bars[cured_pos].set_color('#d62728')
    bars[cured_pos].set_alpha(1.0)
    bars[cured_pos].set_linewidth(2.5)

    # Labels
    ax.set_xlabel('Ounces per Day per Person', fontsize=12, fontweight='bold')
    ax.set_ylabel('Protein Category', fontsize=12, fontweight='bold')
    ax.set_title('Protein Food Consumption by Category (2017-2018)\nCured Meat Highlighted',
                 fontsize=14, fontweight='bold', pad=20)

    # Add value labels
    for i, (cat, val) in enumerate(zip(categories['Food group'], categories['value_oz_per_day'])):
        lbs_year = val * 365 / 16
        ax.text(val + 0.05, i, f'{val:.2f} oz/day ({lbs_year:.1f} lbs/yr)',
                va='center', fontsize=9)

    plt.tight_layout()
    plt.show()

    return categories

protein_comparison = plot_protein_categories_2017(df_protein_clean)

print("\nProtein consumption ranking (2017-2018):")
print(protein_comparison[['Food group', 'value_oz_per_day']].to_string(index=False))

# --- SECTION 6: VISUALIZATION 3 - TEMPORAL HEATMAP ---

def plot_consumption_heatmap(df):
    """
    Heatmap showing consumption patterns across categories and years
    """
    # Select key categories
    key_cats = [
        'Protein foods, cured meat',
        'Protein foods, poultry',
        'Protein foods, meats (beef, veal, pork, lamb, game)',
        'Protein foods, eggs'
    ]

    df_subset = df[df['Food group'].isin(key_cats)]

    # Pivot to create matrix
    pivot = df_subset.pivot_table(
        values='value_oz_per_day',
        index='Food group',
        columns='year',
        aggfunc='first'
    )

    # Create heatmap
    fig, ax = plt.subplots(figsize=(14, 6))

    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlOrRd',
                linewidths=1, linecolor='black', cbar_kws={'label': 'Oz/Day'},
                ax=ax)

    ax.set_title('Protein Consumption Trends: Key Categories (1977-2018)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Protein Category', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.show()

plot_consumption_heatmap(df_protein_clean)

# --- SECTION 7: EXPORT CLEANED DATA ---

# Save cleaned consumption data for use in other notebooks
output_path = 'processed_consumption_data.csv'
df_protein_clean.to_csv(output_path, index=False)
print(f"\nCleaned consumption data saved to: {output_path}")

# Create summary statistics
summary_stats = {
    'cured_meat_2017_oz_day': cured_meat_trend[cured_meat_trend['year'] == 2017]['value_oz_per_day'].values[0],
    'cured_meat_2017_lbs_year': cured_meat_trend[cured_meat_trend['year'] == 2017]['value_lbs_per_year'].values[0],
    'peak_year': int(peak_year),
    'peak_value_oz': peak_value,
    'decline_percent': decline_pct
}

import json
with open('consumption_summary_stats.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

print(f"Summary statistics saved to: consumption_summary_stats.json")
```

---

## Notebook 2: visualization_8_consumption_vs_contamination.ipynb

**Purpose:** Combine consumption data with contamination data to test hypothesis

**Outputs:**
1. Scatter plot: Consumption vs Contamination Rate
2. Correlation analysis
3. Category comparison table
4. Key findings

### Pseudocode:

```python
# ============================================================================
# NOTEBOOK: visualization_8_consumption_vs_contamination.ipynb
# PURPOSE: Combine consumption + contamination data for integrated analysis
# ============================================================================

# --- SECTION 1: SETUP ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
from scipy.stats import pearsonr, spearmanr

# --- SECTION 2: LOAD BOTH DATASETS ---

def load_contamination_data(json_path):
    """
    Load USDA FSIS lab sampling data

    Returns:
        primary_df: Primary test results
    """
    with open(json_path, 'r') as f:
        data = json.load(f)[0]

    primary_df = pd.DataFrame(data['data']['primary_table_data'])

    print(f"Contamination data loaded: {len(primary_df)} samples")
    return primary_df

def load_consumption_data(csv_path):
    """
    Load processed consumption data from previous notebook
    """
    df = pd.read_csv(csv_path)
    print(f"Consumption data loaded: {len(df)} records")
    return df

# Load data
contamination_df = load_contamination_data(
    'labSamplingRteFy2025.json'
)

consumption_df = load_consumption_data('processed_consumption_data.csv')

# Load summary stats
with open('consumption_summary_stats.json', 'r') as f:
    consumption_stats = json.load(f)

print("\nConsumption Summary:")
print(json.dumps(consumption_stats, indent=2))

# --- SECTION 3: CATEGORIZE CONTAMINATION DATA ---

def categorize_contamination_by_protein(df):
    """
    Categorize contamination samples by protein type

    Mapping:
    - sample_source_name contains 'Chicken' or 'Turkey' -> Poultry
    - sample_source_name contains 'Pork' -> Pork
    - sample_source_name contains 'Beef' -> Beef
    - sample_source_name contains 'Sausage' -> Cured meat (subset)
    """
    df_clean = df.copy()

    # Only include samples with Listeria test results
    df_clean = df_clean[df_clean['lm_listeria_analysis'].notna()]

    # Create protein category
    def assign_protein_type(source_name):
        if pd.isna(source_name):
            return 'Unknown'
        source = str(source_name).lower()

        if 'chicken' in source or 'turkey' in source:
            return 'Poultry'
        elif 'pork' in source and 'sausage' in source:
            return 'Cured Meat (Sausage)'
        elif 'pork' in source:
            return 'Pork'
        elif 'beef' in source:
            return 'Beef'
        elif 'sausage' in source:
            return 'Cured Meat (Sausage)'
        elif 'contact' in source.lower():
            return 'Environmental'
        else:
            return 'Other'

    df_clean['protein_category'] = df_clean['sample_source_name'].apply(assign_protein_type)

    # Create positive flag
    df_clean['is_positive'] = df_clean['lm_listeria_analysis'] == 'Positive'

    return df_clean

contamination_categorized = categorize_contamination_by_protein(contamination_df)

# --- SECTION 4: CALCULATE CONTAMINATION RATES BY CATEGORY ---

def calculate_contamination_rates(df):
    """
    Calculate contamination rate for each protein category

    Returns:
        rates_df: DataFrame with contamination rates
    """
    # Exclude environmental samples for this analysis
    df_products = df[df['protein_category'] != 'Environmental'].copy()

    rates = df_products.groupby('protein_category').agg({
        'is_positive': ['sum', 'count', 'mean']
    }).reset_index()

    rates.columns = ['protein_category', 'positive_count', 'total_samples', 'contamination_rate']
    rates['contamination_rate_pct'] = rates['contamination_rate'] * 100

    rates = rates.sort_values('contamination_rate_pct', ascending=False)

    return rates

contamination_rates = calculate_contamination_rates(contamination_categorized)

print("\nContamination Rates by Protein Category:")
print(contamination_rates)

# --- SECTION 5: MATCH CONSUMPTION TO CONTAMINATION ---

def create_matched_dataset():
    """
    Create dataset matching consumption to contamination

    Challenge: Categories don't perfectly align
    - Consumption: "Cured meat", "Poultry", "Meats (beef/pork/lamb)"
    - Contamination: "Cured Meat (Sausage)", "Poultry", "Pork", "Beef"

    Strategy: Best-effort matching with disclaimers
    """

    # Manual matching based on analysis
    matched_data = [
        {
            'category': 'Poultry',
            'consumption_oz_day': 0.81,  # From Table 5
            'consumption_lbs_year': 0.81 * 365 / 16,
            'contamination_rate_pct': contamination_rates[
                contamination_rates['protein_category'] == 'Poultry'
            ]['contamination_rate_pct'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Poultry'
            ]) > 0 else 0,
            'total_samples': contamination_rates[
                contamination_rates['protein_category'] == 'Poultry'
            ]['total_samples'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Poultry'
            ]) > 0 else 0,
            'match_quality': 'Good'
        },
        {
            'category': 'Cured Meat (RTE Sausage)',
            'consumption_oz_day': consumption_stats['cured_meat_2017_oz_day'],
            'consumption_lbs_year': consumption_stats['cured_meat_2017_lbs_year'],
            'contamination_rate_pct': contamination_rates[
                contamination_rates['protein_category'] == 'Cured Meat (Sausage)'
            ]['contamination_rate_pct'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Cured Meat (Sausage)'
            ]) > 0 else 0,
            'total_samples': contamination_rates[
                contamination_rates['protein_category'] == 'Cured Meat (Sausage)'
            ]['total_samples'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Cured Meat (Sausage)'
            ]) > 0 else 0,
            'match_quality': 'Moderate (Sausage is subset of all cured meat)'
        },
        {
            'category': 'Pork (Non-Sausage)',
            'consumption_oz_day': 0.87,  # All meats, use as proxy
            'consumption_lbs_year': 0.87 * 365 / 16,
            'contamination_rate_pct': contamination_rates[
                contamination_rates['protein_category'] == 'Pork'
            ]['contamination_rate_pct'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Pork'
            ]) > 0 else 0,
            'total_samples': contamination_rates[
                contamination_rates['protein_category'] == 'Pork'
            ]['total_samples'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Pork'
            ]) > 0 else 0,
            'match_quality': 'Poor (Consumption includes beef/lamb too)'
        },
        {
            'category': 'Beef',
            'consumption_oz_day': 0.87,  # All meats, use as proxy
            'consumption_lbs_year': 0.87 * 365 / 16,
            'contamination_rate_pct': contamination_rates[
                contamination_rates['protein_category'] == 'Beef'
            ]['contamination_rate_pct'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Beef'
            ]) > 0 else 0,
            'total_samples': contamination_rates[
                contamination_rates['protein_category'] == 'Beef'
            ]['total_samples'].values[0] if len(contamination_rates[
                contamination_rates['protein_category'] == 'Beef'
            ]) > 0 else 0,
            'match_quality': 'Poor (Consumption includes pork/lamb too)'
        }
    ]

    return pd.DataFrame(matched_data)

matched_df = create_matched_dataset()

print("\nMatched Dataset (Consumption + Contamination):")
print(matched_df)

# --- SECTION 6: VISUALIZATION 1 - SCATTER PLOT ---

def plot_consumption_vs_contamination(df):
    """
    Scatter plot: X=Consumption, Y=Contamination Rate
    Bubble size = Sample count
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create scatter plot
    colors = {'Good': '#2ca02c', 'Moderate (Sausage is subset of all cured meat)': '#ff7f0e',
              'Poor (Consumption includes beef/lamb too)': '#d62728',
              'Poor (Consumption includes pork/lamb too)': '#9467bd'}

    for match_quality in df['match_quality'].unique():
        subset = df[df['match_quality'] == match_quality]
        ax.scatter(subset['consumption_lbs_year'],
                   subset['contamination_rate_pct'],
                   s=subset['total_samples'],
                   alpha=0.6,
                   c=[colors.get(match_quality, '#7f7f7f')],
                   edgecolors='black',
                   linewidth=2,
                   label=match_quality)

    # Add labels for each point
    for _, row in df.iterrows():
        ax.annotate(row['category'],
                    xy=(row['consumption_lbs_year'], row['contamination_rate_pct']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=10,
                    fontweight='bold')

    # Labels and title
    ax.set_xlabel('Consumption (lbs per person per year)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Contamination Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Consumption vs Contamination: Do Popular Foods Have Higher Contamination?\\n' +
                 'Bubble Size = Sample Count | Color = Match Quality',
                 fontsize=14, fontweight='bold', pad=20)

    ax.legend(title='Match Quality', loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add disclaimer
    fig.text(0.5, 0.02,
             'DISCLAIMER: Consumption data (2017-18) vs Contamination data (2024-25). ' +
             'Categories do not perfectly align. Interpret as rough comparison.',
             ha='center', fontsize=9, style='italic', color='red')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()

plot_consumption_vs_contamination(matched_df)

# --- SECTION 7: CORRELATION ANALYSIS ---

def calculate_correlation(df):
    """
    Calculate correlation between consumption and contamination

    Note: Only use "Good" match quality for statistical test
    """
    # Filter for good matches only
    good_matches = df[df['match_quality'] == 'Good']

    if len(good_matches) < 2:
        print("Not enough good-quality matches for correlation analysis")
        return None

    # Calculate Pearson correlation
    r_pearson, p_pearson = pearsonr(good_matches['consumption_lbs_year'],
                                     good_matches['contamination_rate_pct'])

    # Calculate Spearman correlation (rank-based)
    r_spearman, p_spearman = spearmanr(good_matches['consumption_lbs_year'],
                                        good_matches['contamination_rate_pct'])

    print("\n" + "="*80)
    print("CORRELATION ANALYSIS (Good Match Quality Only)")
    print("="*80)
    print(f"Pearson Correlation:  r = {r_pearson:.3f}, p-value = {p_pearson:.3f}")
    print(f"Spearman Correlation: rho = {r_spearman:.3f}, p-value = {p_spearman:.3f}")
    print()

    if p_pearson < 0.05:
        if r_pearson > 0.7:
            conclusion = "STRONG POSITIVE: Popular foods have significantly higher contamination"
        elif r_pearson > 0.4:
            conclusion = "MODERATE POSITIVE: Some evidence that popular foods have higher contamination"
        elif r_pearson > 0:
            conclusion = "WEAK POSITIVE: Minimal evidence of correlation"
        else:
            conclusion = "NEGATIVE: Popular foods have LOWER contamination"
    else:
        conclusion = "NO SIGNIFICANT CORRELATION: Consumption does not predict contamination"

    print(f"CONCLUSION: {conclusion}")
    print("="*80)

    return {
        'pearson_r': r_pearson,
        'pearson_p': p_pearson,
        'spearman_rho': r_spearman,
        'spearman_p': p_spearman,
        'conclusion': conclusion
    }

correlation_results = calculate_correlation(matched_df)

# --- SECTION 8: COMPARISON TABLE ---

def create_comparison_table(df):
    """
    Create formatted comparison table
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('tight')
    ax.axis('off')

    # Prepare table data
    table_data = []
    table_data.append(['Category', 'Consumption\\n(lbs/year)', 'Contamination\\nRate (%)',
                       'Samples', 'Match Quality'])

    for _, row in df.iterrows():
        table_data.append([
            row['category'],
            f"{row['consumption_lbs_year']:.1f}",
            f"{row['contamination_rate_pct']:.2f}%",
            f"{int(row['total_samples'])}",
            row['match_quality']
        ])

    table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                     colWidths=[0.25, 0.15, 0.15, 0.1, 0.35])

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Style header row
    for i in range(5):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Color rows by match quality
    for i in range(1, len(table_data)):
        match_quality = table_data[i][4]
        if 'Good' in match_quality:
            color = '#c8e6c9'
        elif 'Moderate' in match_quality:
            color = '#fff9c4'
        else:
            color = '#ffccbc'

        for j in range(5):
            table[(i, j)].set_facecolor(color)

    plt.title('Consumption vs Contamination: Category Comparison',
              fontsize=14, fontweight='bold', pad=20)
    plt.show()

create_comparison_table(matched_df)

# --- SECTION 9: KEY FINDINGS SUMMARY ---

print("\n" + "="*80)
print("KEY FINDINGS: Consumption vs Contamination Analysis")
print("="*80)
print()
print("1. CONSUMPTION PATTERNS (2017-2018):")
print(f"   - Cured meat: {consumption_stats['cured_meat_2017_lbs_year']:.1f} lbs/year")
print(f"   - Poultry: ~18.5 lbs/year")
print(f"   - Declined {abs(consumption_stats['decline_percent']):.1f}% from {consumption_stats['peak_year']} peak")
print()
print("2. CONTAMINATION PATTERNS (FY2025):")
for _, row in contamination_rates.head().iterrows():
    print(f"   - {row['protein_category']}: {row['contamination_rate_pct']:.2f}% ({int(row['positive_count'])}/{int(row['total_samples'])} samples)")
print()
print("3. CORRELATION:")
if correlation_results:
    print(f"   - {correlation_results['conclusion']}")
    print(f"   - Pearson r = {correlation_results['pearson_r']:.3f}, p = {correlation_results['pearson_p']:.3f}")
print()
print("4. LIMITATIONS:")
print("   ⚠️  7-year gap between datasets (2017-18 vs 2024-25)")
print("   ⚠️  Category mismatch (Cured meat ⊃ RTE Sausage)")
print("   ⚠️  Consumption includes raw + RTE for some categories")
print("="*80)

# --- SECTION 10: EXPORT RESULTS ---

matched_df.to_csv('consumption_vs_contamination_matched.csv', index=False)
print("\nMatched dataset saved to: consumption_vs_contamination_matched.csv")

if correlation_results:
    with open('correlation_results.json', 'w') as f:
        json.dump(correlation_results, f, indent=2)
    print("Correlation results saved to: correlation_results.json")
```

---

## Notebook 3: visualization_9_state_map_choropleth.ipynb

**Purpose:** Interactive choropleth map showing contamination by state (contamination data only)

**Outputs:**
1. Interactive Plotly choropleth map
2. State-level statistics table
3. Top 10 states by contamination rate

### Pseudocode:

```python
# ============================================================================
# NOTEBOOK: visualization_9_state_map_choropleth.ipynb
# PURPOSE: Interactive state map showing contamination rates
# DATA: Contamination data ONLY (no consumption data needed)
# ============================================================================

# --- SECTION 1: SETUP ---
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# --- SECTION 2: LOAD CONTAMINATION DATA ---

def load_and_aggregate_by_state(json_path):
    """
    Load contamination data and aggregate by state
    """
    with open(json_path, 'r') as f:
        data = json.load(f)[0]

    df = pd.DataFrame(data['data']['primary_table_data'])

    # Filter for Listeria tests only
    df = df[df['lm_listeria_analysis'].notna()]
    df['is_positive'] = df['lm_listeria_analysis'] == 'Positive'

    # Aggregate by state
    state_stats = df.groupby('establishment_state').agg({
        'form_id': 'count',
        'is_positive': 'sum',
        'establishment_id': 'nunique'
    }).reset_index()

    state_stats.columns = ['state', 'total_samples', 'positive_samples', 'num_facilities']
    state_stats['contamination_rate'] = (state_stats['positive_samples'] /
                                          state_stats['total_samples'] * 100)

    # Filter states with at least 50 samples for statistical validity
    state_stats = state_stats[state_stats['total_samples'] >= 50]

    return state_stats

state_data = load_and_aggregate_by_state(
    'labSamplingRteFy2025.json'
)

print(f"States with sufficient data (≥50 samples): {len(state_data)}")
print("\nTop 10 states by contamination rate:")
print(state_data.nlargest(10, 'contamination_rate')[
    ['state', 'total_samples', 'positive_samples', 'contamination_rate']
])

# --- SECTION 3: CREATE CHOROPLETH MAP ---

def create_choropleth_map(df):
    """
    Create interactive choropleth map using Plotly
    """
    fig = go.Figure(data=go.Choropleth(
        locations=df['state'],
        z=df['contamination_rate'],
        locationmode='USA-states',
        colorscale=[
            [0, 'rgb(255,255,255)'],      # White (0%)
            [0.3, 'rgb(255,220,220)'],    # Light pink
            [0.5, 'rgb(255,150,150)'],    # Pink
            [0.7, 'rgb(255,100,100)'],    # Light red
            [1, 'rgb(200,0,0)']           # Dark red (3%+)
        ],
        zmin=0,
        zmax=3.5,
        colorbar=dict(
            title="Contamination<br>Rate (%)",
            thickness=15,
            len=0.7
        ),
        hovertemplate=(
            '<b>%{location}</b><br>' +
            'Contamination Rate: %{z:.2f}%<br>' +
            'Samples: %{customdata[0]}<br>' +
            'Positives: %{customdata[1]}<br>' +
            'Facilities: %{customdata[2]}<br>' +
            '<extra></extra>'
        ),
        customdata=df[['total_samples', 'positive_samples', 'num_facilities']].values
    ))

    fig.update_layout(
        title={
            'text': 'Listeria Contamination Rate by State (FY2025)<br>' +
                    '<sub>USDA FSIS Lab Sampling: RTE Products & Facilities</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#333'}
        },
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(200, 220, 255)'
        ),
        height=600,
        font=dict(size=12)
    )

    return fig

fig_map = create_choropleth_map(state_data)
fig_map.show()

# Save as HTML for embedding in dashboard
fig_map.write_html('state_contamination_map.html')
print("\nInteractive map saved to: state_contamination_map.html")

# --- SECTION 4: STATE STATISTICS TABLE ---

def create_state_table(df):
    """
    Create formatted table of state statistics
    """
    # Sort by contamination rate
    df_sorted = df.sort_values('contamination_rate', ascending=False).head(20)

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>State</b>', '<b>Total Samples</b>', '<b>Positives</b>',
                    '<b>Rate (%)</b>', '<b>Facilities</b>'],
            fill_color='#4CAF50',
            align='center',
            font=dict(color='white', size=12, family='Arial')
        ),
        cells=dict(
            values=[
                df_sorted['state'],
                df_sorted['total_samples'],
                df_sorted['positive_samples'],
                df_sorted['contamination_rate'].round(2),
                df_sorted['num_facilities']
            ],
            fill_color=[['#f9f9f9', 'white'] * len(df_sorted)],
            align='center',
            font=dict(size=11)
        )
    )])

    fig.update_layout(
        title='Top 20 States by Listeria Contamination Rate',
        height=600
    )

    fig.show()

create_state_table(state_data)

# Export state data
state_data.to_csv('state_contamination_statistics.csv', index=False)
print("State statistics saved to: state_contamination_statistics.csv")
```

---

## Summary: Data Usage Strategy

### What Data Goes Where:

| Visualization | Contamination Data | Consumption Data | Integration Method |
|--------------|-------------------|------------------|-------------------|
| **State Map** | ✅ YES | ❌ NO | State-level aggregation of contamination only |
| **Consumption Trends** | ❌ NO | ✅ YES | Time series of consumption 1977-2018 |
| **Consumption vs Contamination** | ✅ YES | ✅ YES | **COMBINED**: Match categories, test correlation |
| **Product Risk Dashboard** | ✅ YES | ✅ YES | **COMBINED**: Scatter plot showing both |
| **Temporal Trends** | ✅ YES | Optional overlay | Timeline of contamination with consumption overlay |

---

## Modified 3-Map-Implementation-Plan Strategy:

The original plan was to **combine both datasets**, specifically:

### View 1: Geographic Map (Contamination Only)
- **Input:** USDA FSIS lab sampling data
- **Output:** Choropleth map showing contamination rates by state
- **No consumption data needed** - pure contamination visualization

### View 2: Product Risk Analysis (BOTH Datasets Combined)
- **Input:**
  - Contamination data → Calculate rates by product
  - Consumption data → Get consumption by protein type
- **Output:** Scatter plot testing "Do popular foods have higher contamination?"
- **This is the KEY integration point**

### View 3: Timeline (Contamination Primary, Consumption Optional)
- **Input:** Contamination data (monthly trends FY2025)
- **Optional:** Overlay with consumption trend (2009-2018) to show long-term patterns
- **Two separate trend lines** on same chart

---

## Recommendation:

**Create 3 notebooks in this order:**

1. **visualization_7_consumption_trends.ipynb** (NEW)
   - Consumption data ONLY
   - Establishes baseline: "Here's what consumption looks like"
   - Outputs: Clean consumption data for use in notebook 2

2. **visualization_8_consumption_vs_contamination.ipynb** (NEW)
   - **COMBINED analysis**
   - Uses outputs from notebook 1 + raw contamination data
   - Tests hypothesis: Popular foods → higher contamination?
   - THIS IS THE MAIN INTEGRATION

3. **visualization_9_state_map_choropleth.ipynb** (NEW)
   - Contamination data ONLY
   - Interactive map for dashboard
   - No consumption integration needed here

**Does this clarify the strategy? Should we proceed with creating the actual notebooks?**
