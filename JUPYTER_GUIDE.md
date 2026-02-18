# Jupyter Notebook Analysis Guide

This guide explains how to use the analysis commands in Jupyter Notebook.

## File Created

- **`jupyter_analysis_commands.py`** - Contains all the Python commands used for descriptive statistics, organized into 19 logical analysis sections

## How to Use in Jupyter Notebook

### Option 1: Run Entire Script at Once

```python
# In a Jupyter cell, run the entire script
%run jupyter_analysis_commands.py
```

### Option 2: Copy Individual Cells

The file is organized into 19 numbered "CELLS" with clear separators. Each cell can be copied into separate Jupyter cells:

1. **CELL 1:** Import Libraries and Load Data
2. **CELL 2:** Examine Data Structure
3. **CELL 3:** Examine Primary and Secondary Datasets
4. **CELL 4:** View Sample Records
5. **CELL 5:** Missing Value Analysis
6. **CELL 6:** Basic Statistics - Record Counts
7. **CELL 7:** Geographic Distribution
8. **CELL 8:** Project Code Distribution
9. **CELL 9:** Pathogen Detection - Listeria monocytogenes
10. **CELL 10:** Pathogen Detection - Salmonella
11. **CELL 11:** Sample Source Types
12. **CELL 12:** Temporal Analysis - Date Range
13. **CELL 13:** Secondary Dataset - Genetic Characterization
14. **CELL 14:** Listeria Sequence Types (MLST)
15. **CELL 15:** Salmonella Serotypes
16. **CELL 16:** Data Type Analysis
17. **CELL 17:** Positive Cases by State
18. **CELL 18:** Establishments with Positive Results
19. **CELL 19:** Summary Statistics Report

### Option 3: Import as Module

```python
# Import and use individual analysis sections
import jupyter_analysis_commands

# Or import specific functions if you modify it to include function definitions
```

## Prerequisites

### Required File
Make sure the data file is in the same directory as your notebook:
```
usda_fsis_data_product_establishment_specific_laboratory_sampling_rte_product_fy2025.json
```

### Required Libraries
All analysis uses only Python standard library:
- `json` - Built-in
- `collections` (Counter, defaultdict) - Built-in
- `datetime` - Built-in

**No external dependencies required!** (pandas, numpy, matplotlib are not needed for this analysis)

## Quick Start

1. Open Jupyter Notebook or JupyterLab
2. Create a new notebook in the `listeria-tracker` directory
3. Copy and run the cells in order, or:

```python
# Single command to run everything
%run jupyter_analysis_commands.py
```

## Output

Each cell produces formatted console output including:

- **Data structure summaries**
- **Statistical tables**
- **Distribution charts (text-based)**
- **Geographic breakdowns**
- **Pathogen detection rates**
- **Genetic diversity metrics**
- **Facility risk assessments**
- **Comprehensive summary report**

## Tips for Jupyter Usage

1. **Run cells sequentially** - Later cells depend on variables from earlier cells
2. **Use markdown cells** - Add markdown cells between code cells to annotate your analysis
3. **Modify as needed** - Adjust `most_common(N)` values to see more/fewer results
4. **Export results** - Copy output to markdown cells for reports
5. **Save intermediate results** - Assign outputs to variables for further analysis:

```python
# Example: Save state analysis for further use
state_summary = {state: count for state, count in states.most_common()}
```

## Advanced Usage

### Creating Visualizations

If you want to add visualizations, install pandas and matplotlib:

```python
# Install in Jupyter
!pip install pandas matplotlib seaborn

# Then you can convert to DataFrames
import pandas as pd
primary_df = pd.DataFrame(primary_data)
secondary_df = pd.DataFrame(secondary_data)

# Create visualizations
import matplotlib.pyplot as plt
primary_df['establishment_state'].value_counts().head(15).plot(kind='bar')
plt.title('Top 15 States by Sample Count')
plt.show()
```

### Filtering Data

```python
# Example: Filter for positive Listeria samples only
lm_positives = [r for r in primary_data if r['lm_listeria_analysis'] == 'Positive']
print(f"Total Listeria positives: {len(lm_positives)}")

# Analyze positive samples by state
positive_states = Counter([r['establishment_state'] for r in lm_positives])
print(positive_states.most_common())
```

### Joining Primary and Secondary Data

```python
# Create lookup dictionary for genetic data
genetic_data = {r['form_id']: r for r in secondary_data}

# Enrich positive samples with genetic information
for record in lm_positives:
    form_id = record['form_id']
    if form_id in genetic_data:
        record['genetic_info'] = genetic_data[form_id]
```

## Troubleshooting

**Error: File not found**
- Ensure the JSON file is in the same directory
- Use full path: `open('/full/path/to/file.json')`

**Error: Memory issues**
- The dataset is ~48MB, should be fine for most systems
- If issues persist, process data in chunks

**Error: Variable not defined**
- Run cells in order from the beginning
- Cell 1 must be run first to load data

## Next Steps

After running the analysis:

1. Review the comprehensive findings in `docs/1-research-findings.md`
2. Examine the dashboard proposal (6 visualization views)
3. Review the implementation skeleton in `main.py`
4. Await approval to create detailed implementation plan in `docs/2-plan.md`

## Questions?

Refer to:
- **Research findings:** `docs/1-research-findings.md`
- **Original research task:** `docs/1-research.md`
- **Implementation skeleton:** `main.py`
