# Interactive Contamination Map - Implementation Plan

## Project Overview

**Goal:** Create an interactive web-based map showing Listeria contamination rates by state, integrated with USDA consumption data to test whether popular foods have higher contamination rates.

**Dataset:** USDA FSIS Lab Sampling Data FY2025 (27,211 samples, 208 Listeria positives, 53 states/territories)

**Key Question:** Do popular food products (chicken, beef, pork) show higher contamination rates?

---

## Technical Stack

### Recommended: Python + Plotly Dash

**Core Libraries:**
- **Plotly**: Interactive choropleth maps, charts, graphs
- **Dash**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Statistical calculations

**Why This Stack:**
- Rich interactive mapping capabilities
- No JavaScript required
- Easy deployment (local or cloud)
- Integrated with data analysis workflow
- Excellent documentation and community support

**Installation:**
```bash
pip install dash plotly pandas numpy requests
```

---

## Architecture Overview

```
listeria-tracker/
├── app.py                          # Main Dash application
├── data/
│   ├── loader.py                   # Load USDA FSIS JSON data
│   ├── processor.py                # Clean and transform data
│   ├── consumption_data.py         # USDA consumption data integration
│   └── cache/                      # Processed data cache
├── analysis/
│   ├── state_analysis.py           # State-level aggregations
│   ├── product_analysis.py         # Product type analysis
│   ├── correlation.py              # Consumption vs contamination
│   └── statistics.py               # Statistical tests
├── visualization/
│   ├── map_view.py                 # Interactive state map
│   ├── product_dashboard.py        # Product risk dashboard
│   ├── timeline.py                 # Temporal analysis
│   └── components.py               # Reusable UI components
├── assets/
│   ├── styles.css                  # Custom styling
│   └── logo.png                    # Dashboard branding
├── docs/
│   ├── 1-research-findings.md
│   ├── 2-data-comparison-analysis.md
│   └── 3-map-implementation-plan.md (this file)
└── tests/
    ├── test_data_loader.py
    └── test_analysis.py
```

---

## Phase 1: Data Processing Pipeline

### Step 1.1: Load and Parse USDA FSIS Data

**File:** `data/loader.py`

**Functionality:**
```python
def load_fsis_data(json_path):
    """
    Load USDA FSIS lab sampling data

    Returns:
        primary_df: Primary test results (27,211 records)
        secondary_df: Secondary characterization (443 records)
        metadata: Dataset metadata
    """
    # Parse JSON
    # Convert to pandas DataFrames
    # Validate data structure
    # Cache processed data
```

**Key Fields to Extract:**
- `form_id`, `sample_number`
- `establishment_id`, `establishment_name`, `establishment_state`
- `collection_date`
- `sample_source_name`
- `lm_listeria_analysis`, `salmonella_sp_analysis`
- `project_code`, `project_name`

**Data Validation:**
- Check for missing critical fields
- Validate date formats
- Ensure state codes are valid (50 states + DC, PR, GU)
- Flag unusual detection rates

---

### Step 1.2: Clean and Transform Data

**File:** `data/processor.py`

**Transformations:**

1. **Convert Data Types:**
   ```python
   df['collection_date'] = pd.to_datetime(df['collection_date'])
   df['establishment_id'] = df['establishment_id'].astype(int)
   df['lm_listeria_analysis'] = df['lm_listeria_analysis'].astype('category')
   ```

2. **Create Derived Fields:**
   ```python
   # Binary contamination flag
   df['is_listeria_positive'] = df['lm_listeria_analysis'] == 'Positive'

   # Categorize sample types
   def categorize_sample(source_name):
       if 'Contact Surface' in source_name:
           return 'Environmental-Contact'
       elif 'Non/Product Contact' in source_name:
           return 'Environmental-NonContact'
       elif source_name.startswith('Product-RTE'):
           return 'Product'
       else:
           return 'Other'

   df['sample_category'] = df['sample_source_name'].apply(categorize_sample)

   # Extract protein type
   def extract_protein(source_name):
       if 'Chicken' in source_name:
           return 'Chicken'
       elif 'Pork' in source_name:
           return 'Pork'
       elif 'Beef' in source_name:
           return 'Beef'
       elif 'Turkey' in source_name:
           return 'Turkey'
       else:
           return 'Other/Mixed'

   df['protein_type'] = df['sample_source_name'].apply(extract_protein)
   ```

3. **Handle Missing Values:**
   ```python
   # Fill missing states with 'Unknown'
   df['establishment_state'].fillna('Unknown', inplace=True)

   # Drop records with no test results
   df = df[df['lm_listeria_analysis'].notna()]
   ```

---

### Step 1.3: Integrate USDA Consumption Data

**File:** `data/consumption_data.py`

**Data Source:** USDA Economic Research Service (ERS) - Food Availability Data System

**URL:** https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/

**Data to Collect (FY2025 / Calendar Year 2024):**
```python
consumption_data = {
    'Chicken': {
        'per_capita_lbs': 60.4,  # lbs per person per year
        'total_production_lbs': 20_000_000_000,  # US total
        'rank': 1
    },
    'Beef': {
        'per_capita_lbs': 56.7,
        'total_production_lbs': 18_700_000_000,
        'rank': 2
    },
    'Pork': {
        'per_capita_lbs': 25.2,
        'total_production_lbs': 8_300_000_000,
        'rank': 3
    },
    'Turkey': {
        'per_capita_lbs': 15.3,
        'total_production_lbs': 5_050_000_000,
        'rank': 4
    }
}
```

**Implementation:**
```python
def get_usda_consumption_data():
    """
    Fetch USDA ERS consumption data

    Options:
    1. Manual CSV from ERS website
    2. API call (if available)
    3. Hardcoded reference values

    Returns:
        DataFrame with columns: protein_type, per_capita_lbs, production_lbs, rank
    """
    pass

def merge_consumption_with_contamination(contamination_df, consumption_df):
    """
    Merge contamination rates with consumption data

    Returns:
        DataFrame with columns:
        - protein_type
        - contamination_rate (%)
        - per_capita_consumption (lbs)
        - correlation_score
    """
    pass
```

---

## Phase 2: State-Level Analysis

### Step 2.1: Aggregate State Statistics

**File:** `analysis/state_analysis.py`

**Key Metrics by State:**

```python
def calculate_state_metrics(df):
    """
    Calculate contamination metrics for each state

    Returns DataFrame with columns:
    - state_code: Two-letter state abbreviation
    - total_samples: Number of samples tested
    - positive_listeria: Number of Listeria positives
    - positive_salmonella: Number of Salmonella positives
    - contamination_rate: Percentage of positive samples
    - num_facilities: Unique establishments tested
    - high_risk_facilities: Facilities with 2+ positives
    - environmental_rate: Environmental sample positive rate
    - product_rate: Product sample positive rate
    """

    state_metrics = df.groupby('establishment_state').agg({
        'form_id': 'count',  # total samples
        'is_listeria_positive': 'sum',  # positive count
        'establishment_id': 'nunique'  # unique facilities
    }).rename(columns={
        'form_id': 'total_samples',
        'is_listeria_positive': 'positive_listeria',
        'establishment_id': 'num_facilities'
    })

    state_metrics['contamination_rate'] = (
        state_metrics['positive_listeria'] / state_metrics['total_samples'] * 100
    )

    return state_metrics
```

**Current Data Insights (from analysis):**
```
Top 5 States by Contamination Rate:
1. South Carolina: 2.97% (10/337 samples, 15 facilities)
2. Maryland: 2.85% (7/246 samples, 17 facilities)
3. Georgia: 1.94% (20/1033 samples, 60 facilities)
4. Oklahoma: 1.70% (15/882 samples, 40 facilities)
5. Illinois: 1.18% (25/2125 samples, 136 facilities)

National Average: 0.77% (208/27,124 samples)
```

---

### Step 2.2: State-Level Product Analysis

**Questions to Answer:**
1. Which protein types are most contaminated in each state?
2. Do high-consumption states have higher contamination?
3. Are coastal vs inland states different?

**Implementation:**
```python
def analyze_state_products(df, consumption_df):
    """
    Analyze which products are contaminated in each state

    Returns:
        state_product_matrix: State × Protein Type contamination rates
    """

    pivot = df.pivot_table(
        values='is_listeria_positive',
        index='establishment_state',
        columns='protein_type',
        aggfunc=['count', 'sum', 'mean']
    )

    return pivot
```

---

## Phase 3: Product Risk Analysis

### Step 3.1: Calculate Product Contamination Rates

**File:** `analysis/product_analysis.py`

**Current Data (from earlier analysis):**
```python
product_rates = {
    'RTE Diced Chicken': {'samples': 441, 'positives': 8, 'rate': 1.81},
    'RTE Pork Sausage': {'samples': 952, 'positives': 8, 'rate': 0.84},
    'RTE Beef': {'samples': 498, 'positives': 2, 'rate': 0.40},
    'RTE Not Sliced Pork': {'samples': 599, 'positives': 4, 'rate': 0.67},
    'Environmental Non-Contact': {'samples': 2600, 'positives': 92, 'rate': 3.54}
}
```

**Key Finding:** Environmental samples have 3.54% contamination vs 0.3-1.8% for products

---

### Step 3.2: Consumption vs Contamination Correlation

**File:** `analysis/correlation.py`

**Statistical Test:**
```python
def test_consumption_contamination_correlation(product_df, consumption_df):
    """
    Test hypothesis: Popular foods have higher contamination

    Method: Pearson correlation coefficient
    H0: No correlation between consumption and contamination
    H1: Positive correlation exists

    Returns:
        correlation_coefficient: r value
        p_value: Statistical significance
        conclusion: Interpretation
    """

    from scipy.stats import pearsonr

    # Merge data
    merged = product_df.merge(consumption_df, on='protein_type')

    # Calculate correlation
    r, p = pearsonr(merged['per_capita_consumption'], merged['contamination_rate'])

    interpretation = {
        'correlation': r,
        'p_value': p,
        'significant': p < 0.05,
        'conclusion': interpret_correlation(r, p)
    }

    return interpretation

def interpret_correlation(r, p):
    if p >= 0.05:
        return "No statistically significant correlation found"
    elif r > 0.7:
        return "Strong positive correlation: Popular foods ARE more contaminated"
    elif r > 0.4:
        return "Moderate positive correlation: Some evidence of higher contamination"
    elif r > 0:
        return "Weak positive correlation: Minimal evidence"
    else:
        return "Negative correlation: Popular foods LESS contaminated"
```

---

## Phase 4: Interactive Map Visualization

### Step 4.1: Choropleth Map - State Contamination

**File:** `visualization/map_view.py`

**Technology:** Plotly Choropleth (built-in US state boundaries)

**Design:**
```python
import plotly.graph_objects as go

def create_state_contamination_map(state_metrics_df):
    """
    Create interactive choropleth map of US states

    Features:
    - Color scale: White (0%) to Dark Red (3%+)
    - Hover tooltips: State name, contamination rate, sample count
    - Click interaction: Drill down to state details
    """

    fig = go.Figure(data=go.Choropleth(
        locations=state_metrics_df['state_code'],
        z=state_metrics_df['contamination_rate'],
        locationmode='USA-states',
        colorscale=[
            [0, 'rgb(255,255,255)'],      # White (0%)
            [0.3, 'rgb(255,220,220)'],    # Light pink
            [0.5, 'rgb(255,150,150)'],    # Pink
            [0.7, 'rgb(255,100,100)'],    # Light red
            [1, 'rgb(200,0,0)']           # Dark red (3%+)
        ],
        colorbar_title="Contamination<br>Rate (%)",
        hovertemplate=(
            '<b>%{location}</b><br>' +
            'Contamination Rate: %{z:.2f}%<br>' +
            'Samples: %{customdata[0]}<br>' +
            'Positives: %{customdata[1]}<br>' +
            'Facilities: %{customdata[2]}<br>' +
            '<extra></extra>'
        ),
        customdata=state_metrics_df[['total_samples', 'positive_listeria', 'num_facilities']].values
    ))

    fig.update_layout(
        title_text='Listeria Contamination Rate by State (FY2025)',
        geo_scope='usa',
        height=600,
        font=dict(size=14)
    )

    return fig
```

**Visual Elements:**
- Color intensity = contamination rate
- State boundaries clearly visible
- Hover shows detailed stats
- Click state → drill down to facility details

---

### Step 4.2: Product Risk Dashboard

**File:** `visualization/product_dashboard.py`

**Layout Components:**

**Panel 1: Consumption vs Contamination Scatter Plot**
```python
def create_consumption_contamination_plot(merged_df):
    """
    Scatter plot: X=Consumption, Y=Contamination Rate

    Visual:
    - X-axis: Per capita consumption (lbs/year)
    - Y-axis: Contamination rate (%)
    - Bubble size: Total samples tested
    - Color: Protein type
    - Trendline: Linear regression
    """

    fig = px.scatter(
        merged_df,
        x='per_capita_consumption',
        y='contamination_rate',
        size='total_samples',
        color='protein_type',
        hover_data=['total_samples', 'positive_count'],
        title='Does Popular = Contaminated?',
        labels={
            'per_capita_consumption': 'Annual Consumption (lbs per person)',
            'contamination_rate': 'Contamination Rate (%)'
        },
        trendline='ols'  # Ordinary least squares regression
    )

    # Add correlation coefficient annotation
    r, p = calculate_correlation(merged_df)
    fig.add_annotation(
        text=f'Correlation: r={r:.3f}, p={p:.3f}',
        xref='paper', yref='paper',
        x=0.02, y=0.98,
        showarrow=False
    )

    return fig
```

**Panel 2: Product Category Bar Chart**
```python
def create_product_risk_bars(product_metrics_df):
    """
    Horizontal bar chart of product contamination rates

    Sorted by rate (descending)
    Color: Red gradient by rate
    Annotations: Sample counts
    """

    fig = px.bar(
        product_metrics_df.sort_values('contamination_rate', ascending=True),
        x='contamination_rate',
        y='product_category',
        orientation='h',
        color='contamination_rate',
        color_continuous_scale='Reds',
        title='Product Contamination Risk Rankings',
        labels={'contamination_rate': 'Contamination Rate (%)'}
    )

    return fig
```

**Panel 3: Environmental vs Product Comparison**
```python
def create_sample_type_comparison(df):
    """
    Box plot comparing contamination rates:
    - Product samples
    - Contact surface samples
    - Non-contact surface samples
    """

    fig = px.box(
        df,
        x='sample_category',
        y='contamination_rate',
        color='sample_category',
        title='Contamination Rates by Sample Type',
        points='all'  # Show individual data points
    )

    return fig
```

---

### Step 4.3: Timeline Analysis

**File:** `visualization/timeline.py`

**Visualization 1: Daily Detection Rate**
```python
def create_temporal_trend(df):
    """
    Line chart: Contamination rate over time

    Features:
    - X-axis: Date (Oct 2024 - Sep 2025)
    - Y-axis: Rolling 7-day average contamination rate
    - Lines: Separate for Listeria, Salmonella
    - Annotations: Peak contamination periods
    """

    # Calculate daily rates
    daily = df.groupby('collection_date').agg({
        'form_id': 'count',
        'is_listeria_positive': 'sum'
    })
    daily['rate'] = daily['is_listeria_positive'] / daily['form_id'] * 100

    # Apply rolling average
    daily['rate_rolling'] = daily['rate'].rolling(window=7, center=True).mean()

    fig = px.line(
        daily.reset_index(),
        x='collection_date',
        y='rate_rolling',
        title='Contamination Rate Trend (7-day rolling average)',
        labels={'rate_rolling': 'Contamination Rate (%)'}
    )

    return fig
```

**Visualization 2: Calendar Heatmap**
```python
def create_calendar_heatmap(df):
    """
    Calendar view: Daily positive detection counts

    Layout: Week rows × Day columns
    Color: Number of positives detected
    """

    # Aggregate by date
    daily_counts = df[df['is_listeria_positive']].groupby('collection_date').size()

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        x=daily_counts.index.dayofweek,
        y=daily_counts.index.week,
        z=daily_counts.values,
        colorscale='Reds',
        hovertemplate='Date: %{x}<br>Positives: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title='Contamination Detection Calendar',
        xaxis=dict(title='Day of Week'),
        yaxis=dict(title='Week of Year')
    )

    return fig
```

---

## Phase 5: Dash Application Integration

### Step 5.1: Main Application Structure

**File:** `app.py`

```python
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from data.loader import load_fsis_data
from data.processor import process_data
from data.consumption_data import get_consumption_data, merge_data
from analysis.state_analysis import calculate_state_metrics
from analysis.product_analysis import calculate_product_metrics
from analysis.correlation import test_correlation
from visualization.map_view import create_state_contamination_map
from visualization.product_dashboard import (
    create_consumption_contamination_plot,
    create_product_risk_bars
)
from visualization.timeline import create_temporal_trend

# Initialize app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Load data (cached)
primary_df, secondary_df, metadata = load_fsis_data('usda_fsis_data_product_establishment_specific_laboratory_sampling_rte_product_fy2025.json')
processed_df = process_data(primary_df)
consumption_df = get_consumption_data()
merged_df = merge_data(processed_df, consumption_df)

# Calculate metrics
state_metrics = calculate_state_metrics(processed_df)
product_metrics = calculate_product_metrics(processed_df, consumption_df)
correlation_result = test_correlation(merged_df)

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Listeria Tracker: Interactive Contamination Map", className="text-center mb-4"),
            html.P(
                f"USDA FSIS Lab Sampling Data FY2025 | {len(processed_df):,} samples from {processed_df['establishment_id'].nunique():,} facilities",
                className="text-center text-muted"
            )
        ])
    ]),

    # Key Findings Card
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Key Findings")),
                dbc.CardBody([
                    html.H5(f"National Contamination Rate: {state_metrics['contamination_rate'].mean():.2f}%"),
                    html.P(f"Correlation (Consumption vs Contamination): r={correlation_result['correlation']:.3f}, p={correlation_result['p_value']:.3f}"),
                    html.P(correlation_result['conclusion'], className="text-info")
                ])
            ])
        ])
    ], className="mb-4"),

    # Tab Navigation
    dbc.Tabs([
        dbc.Tab(label="State Map", tab_id="map-tab"),
        dbc.Tab(label="Product Risk", tab_id="product-tab"),
        dbc.Tab(label="Timeline", tab_id="timeline-tab"),
        dbc.Tab(label="Data Explorer", tab_id="data-tab")
    ], id="tabs", active_tab="map-tab"),

    # Tab content
    html.Div(id="tab-content", className="mt-4")
], fluid=True)

# Callbacks for tab switching
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "map-tab":
        return render_map_tab(state_metrics)
    elif active_tab == "product-tab":
        return render_product_tab(product_metrics, merged_df)
    elif active_tab == "timeline-tab":
        return render_timeline_tab(processed_df)
    elif active_tab == "data-tab":
        return render_data_tab(processed_df)

def render_map_tab(state_metrics):
    return dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='state-map',
                figure=create_state_contamination_map(state_metrics),
                style={'height': '600px'}
            )
        ], width=12),
        dbc.Col([
            html.H5("Top 10 States by Contamination Rate"),
            html.Div(id='state-details')
        ], width=12)
    ])

def render_product_tab(product_metrics, merged_df):
    return dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=create_consumption_contamination_plot(merged_df)
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                figure=create_product_risk_bars(product_metrics)
            )
        ], width=6)
    ])

def render_timeline_tab(df):
    return dbc.Row([
        dbc.Col([
            dcc.Graph(figure=create_temporal_trend(df))
        ], width=12)
    ])

def render_data_tab(df):
    return dbc.Row([
        dbc.Col([
            html.H5("Raw Data Explorer"),
            # Add data table with filters
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
```

---

### Step 5.2: Interactive Features

**Feature 1: State Click → Facility Details**
```python
@app.callback(
    Output('state-details', 'children'),
    Input('state-map', 'clickData')
)
def display_state_details(clickData):
    if not clickData:
        return "Click a state to see facility details"

    state = clickData['points'][0]['location']
    state_data = processed_df[processed_df['establishment_state'] == state]

    # Facility table
    facility_summary = state_data.groupby('establishment_name').agg({
        'form_id': 'count',
        'is_listeria_positive': 'sum'
    }).reset_index()

    return dbc.Table.from_dataframe(
        facility_summary.head(10),
        striped=True,
        bordered=True,
        hover=True
    )
```

**Feature 2: Date Range Filter**
```python
@app.callback(
    Output('state-map', 'figure'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_map_by_date(start_date, end_date):
    filtered_df = processed_df[
        (processed_df['collection_date'] >= start_date) &
        (processed_df['collection_date'] <= end_date)
    ]

    state_metrics = calculate_state_metrics(filtered_df)
    return create_state_contamination_map(state_metrics)
```

**Feature 3: Product Type Filter**
```python
@app.callback(
    Output('product-risk-chart', 'figure'),
    Input('protein-dropdown', 'value')
)
def filter_by_protein(selected_protein):
    if selected_protein == 'All':
        filtered_df = processed_df
    else:
        filtered_df = processed_df[processed_df['protein_type'] == selected_protein]

    product_metrics = calculate_product_metrics(filtered_df)
    return create_product_risk_bars(product_metrics)
```

---

## Phase 6: Deployment

### Option 1: Local Deployment (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Access at http://localhost:8050
```

### Option 2: Cloud Deployment (Production)

**Heroku Deployment:**
```bash
# Create Procfile
echo "web: gunicorn app:server" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
heroku create listeria-tracker
git push heroku main
```

**Alternative: Render.com (Free Tier)**
- Connect GitHub repo
- Auto-deploy on push
- Custom domain support

---

## Data Update Strategy

### Quarterly Updates (USDA releases data quarterly)

**Process:**
1. Download new JSON file from USDA FSIS
2. Run data validation checks
3. Append to existing dataset
4. Recalculate all metrics
5. Update dashboard

**Automation Script:** `scripts/update_data.py`
```python
def check_for_updates():
    """
    Check USDA FSIS website for new data releases
    Download and integrate if available
    """
    pass
```

---

## Testing Strategy

### Unit Tests

**File:** `tests/test_data_loader.py`
```python
def test_load_fsis_data():
    df = load_fsis_data('test_data.json')
    assert len(df) > 0
    assert 'establishment_state' in df.columns

def test_contamination_rate_calculation():
    test_df = create_test_dataframe()
    rate = calculate_contamination_rate(test_df)
    assert 0 <= rate <= 100
```

### Integration Tests
```python
def test_map_rendering():
    state_metrics = calculate_state_metrics(test_df)
    fig = create_state_contamination_map(state_metrics)
    assert fig is not None
```

---

## Success Metrics

### User Engagement
- Page views
- Time on site
- State clicks (interactions)
- Filter usage

### Analytical Value
- Successfully answers: "Do popular foods have higher contamination?"
- Correlation coefficient with statistical significance
- Identifies high-risk states and products
- Tracks temporal trends

### Technical Performance
- Page load time < 3 seconds
- Map rendering < 1 second
- Data refresh < 5 seconds

---

## Timeline

### Week 1: Data Processing
- ✅ Day 1-2: Load and validate data
- ✅ Day 3-4: Clean and transform data
- ✅ Day 5: Integrate consumption data
- ✅ Day 6-7: Calculate state and product metrics

### Week 2: Visualization
- Day 1-3: Build choropleth map
- Day 4-5: Build product risk dashboard
- Day 6-7: Build timeline visualizations

### Week 3: Integration
- Day 1-3: Integrate all components in Dash
- Day 4-5: Add interactivity (callbacks)
- Day 6-7: Styling and polish

### Week 4: Testing & Deployment
- Day 1-3: Testing and bug fixes
- Day 4-5: Documentation
- Day 6-7: Deploy to production

**Total Timeline: 4 weeks**

---

## Budget & Resources

### Development
- **Free:** All open-source libraries
- **Cloud Hosting:** $0-10/month (Render free tier or Heroku Hobby)
- **Domain:** $12/year (optional)

### Data Sources
- **USDA FSIS Lab Data:** Free (public domain)
- **USDA ERS Consumption Data:** Free (government data)

### Total Cost: $0-$132/year

---

## Next Steps

### Immediate Actions:
1. ✅ Create `data/loader.py` - Load JSON data
2. ✅ Create `data/processor.py` - Clean and transform
3. ✅ Create `analysis/state_analysis.py` - Calculate state metrics
4. 🔄 Obtain USDA consumption data (manual CSV or API)
5. 🔄 Build first prototype: State map only
6. 🔄 Iterate and add features

### Phase Milestones:
- **Milestone 1:** Data pipeline working (1 week)
- **Milestone 2:** Basic map rendering (2 weeks)
- **Milestone 3:** Full dashboard with all tabs (3 weeks)
- **Milestone 4:** Deployed and accessible (4 weeks)

---

## Appendix A: Key Insights from Current Data

### State Rankings (Contamination Rate, min 50 samples):
1. **South Carolina:** 2.97% (10/337) - 3.8× national average
2. **Maryland:** 2.85% (7/246) - 3.7× national average
3. **Georgia:** 1.94% (20/1033) - 2.5× national average
4. **Oklahoma:** 1.70% (15/882) - 2.2× national average
5. **Illinois:** 1.18% (25/2125) - 1.5× national average

### Product Rankings (Contamination Rate):
1. **Environmental Non-Contact:** 3.54% (92/2600) - Highest risk
2. **RTE Diced Chicken:** 1.81% (8/441)
3. **RTE Pork Sausage:** 0.84% (8/952)
4. **RTE Not Sliced Pork:** 0.67% (4/599)
5. **Environmental Contact:** 0.57% (58/10135)

### Key Finding:
**Environmental contamination (3.54%) is 5× higher than product contamination (0.3-1.8%)**

This suggests facilities have sanitation issues that don't always translate to product contamination - indicating effective controls between environment and product.

---

## Appendix B: USDA Consumption Data Sources

### Primary Source: USDA ERS Food Availability System
**URL:** https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/

**Data Tables:**
- Loss-Adjusted Food Availability (per capita)
- Meat, Poultry, and Fish
- Direct Download: Excel spreadsheets

### Alternative: USDA Agricultural Statistics
**URL:** https://www.nass.usda.gov/Statistics_by_Subject/

**Data Available:**
- Livestock slaughter numbers
- Meat production volumes
- State-level production

### Reference Values (2024 estimates):
- **Chicken:** 60.4 lbs/person/year
- **Beef:** 56.7 lbs/person/year
- **Pork:** 25.2 lbs/person/year
- **Turkey:** 15.3 lbs/person/year

Source: USDA ERS Loss-Adjusted Food Availability documentation

---

## Questions?

Contact: [Project Team]
Last Updated: February 17, 2026
Version: 1.0
