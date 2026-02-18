"""
USDA FSIS Listeria Tracker - Jupyter Notebook Analysis Commands

This file contains all the Python commands used for descriptive statistics
and data analysis. Copy these code blocks into Jupyter notebook cells.

Author: Claude Code Analysis
Date: 2026-01-16
"""

# ============================================================================
# CELL 1: Import Libraries and Load Data
# ============================================================================

import json
from collections import Counter, defaultdict
from datetime import datetime

# Load JSON file
print("Loading data...")
with open('usda_fsis_data_product_establishment_specific_laboratory_sampling_rte_product_fy2025.json', 'r') as f:
    data = json.load(f)

print("Data loaded successfully!")


# ============================================================================
# CELL 2: Examine Data Structure
# ============================================================================

# Check overall structure
print('=== DATA STRUCTURE ===')
print(f'Type: {type(data)}')
print(f'Number of top-level records: {len(data)}')

# Check keys at root level
if isinstance(data, list) and len(data) > 0:
    print(f'Top-level keys: {list(data[0].keys())}')

# Extract the data section
root_data = data[0]['data']
print(f'\n=== DATA SECTION KEYS ===')
print(f'Keys in data section: {list(root_data.keys())}')


# ============================================================================
# CELL 3: Examine Primary and Secondary Datasets
# ============================================================================

# Extract datasets
primary_data = root_data['primary_table_data']
secondary_data = root_data['secondary_table_data']

print("="*80)
print("PRIMARY DATASET")
print("="*80)
print(f"Total records: {len(primary_data):,}")

if len(primary_data) > 0:
    # Get column names
    columns = list(primary_data[0].keys())
    print(f"Total columns: {len(columns)}")
    print(f"\nColumn names:")
    for i, col in enumerate(columns, 1):
        print(f"  {i:3d}. {col}")

print("\n" + "="*80)
print("SECONDARY DATASET")
print("="*80)
print(f"Total records: {len(secondary_data):,}")

if len(secondary_data) > 0:
    columns = list(secondary_data[0].keys())
    print(f"Total columns: {len(columns)}")
    print(f"\nColumn names:")
    for i, col in enumerate(columns, 1):
        print(f"  {i:3d}. {col}")


# ============================================================================
# CELL 4: View Sample Records
# ============================================================================

print("="*80)
print("SAMPLE PRIMARY RECORD")
print("="*80)
for key, value in list(primary_data[0].items())[:25]:
    print(f"{key:40s}: {value}")

print("\n" + "="*80)
print("SAMPLE SECONDARY RECORD")
print("="*80)
if len(secondary_data) > 0:
    for key, value in list(secondary_data[0].items())[:20]:
        print(f"{key:50s}: {value}")


# ============================================================================
# CELL 5: Missing Value Analysis
# ============================================================================

print("="*80)
print("MISSING VALUE ANALYSIS - PRIMARY DATASET")
print("="*80)

null_counts = defaultdict(int)
for record in primary_data:
    for key, value in record.items():
        if value is None or value == "NULL" or value == "":
            null_counts[key] += 1

print(f"\nColumns with missing values (sorted by % missing):")
for col, count in sorted(null_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(primary_data)) * 100
    print(f"  {col:45s}: {count:6,} ({pct:5.1f}%)")


# ============================================================================
# CELL 6: Basic Statistics - Record Counts
# ============================================================================

print("="*80)
print("BASIC STATISTICS")
print("="*80)

print(f"\nTotal Records:")
print(f"  Primary Dataset: {len(primary_data):,}")
print(f"  Secondary Dataset: {len(secondary_data):,}")

# Unique establishments
unique_establishments = len(set([r['establishment_id'] for r in primary_data
                                 if r['establishment_id'] not in [None, 'NULL', '']]))
print(f"\nUnique Establishments: {unique_establishments:,}")

# Unique states
unique_states = len(set([r['establishment_state'] for r in primary_data
                         if r['establishment_state'] not in [None, 'NULL', '']]))
print(f"States/Territories Covered: {unique_states}")

# Unique form IDs
unique_forms = len(set([r['form_id'] for r in primary_data
                        if r['form_id'] not in [None, 'NULL', '']]))
print(f"Unique Form IDs (Samples): {unique_forms:,}")


# ============================================================================
# CELL 7: Geographic Distribution
# ============================================================================

print("="*80)
print("GEOGRAPHIC DISTRIBUTION")
print("="*80)

# Count samples by state
states = Counter([r['establishment_state'] for r in primary_data
                  if r['establishment_state'] not in [None, 'NULL', '']])

print(f"\nTop 15 States (by sample count):")
for state, count in states.most_common(15):
    pct = (count / len(primary_data)) * 100
    print(f"  {state:5s}: {count:5,} samples ({pct:5.2f}%)")

print(f"\nAll {len(states)} States/Territories:")
for state, count in sorted(states.items()):
    print(f"  {state}: {count:,}")


# ============================================================================
# CELL 8: Project Code Distribution
# ============================================================================

print("="*80)
print("SAMPLING PROJECT DISTRIBUTION")
print("="*80)

projects = Counter([r['project_code'] for r in primary_data
                   if r['project_code'] not in [None, 'NULL', '']])

print(f"\nAll Project Codes (Total: {len(projects)}):")
for proj, count in projects.most_common():
    pct = (count / len(primary_data)) * 100
    project_name = primary_data[0]['project_name'] if primary_data else ""
    print(f"  {proj:20s}: {count:5,} ({pct:5.2f}%)")


# ============================================================================
# CELL 9: Pathogen Detection Results - Listeria monocytogenes
# ============================================================================

print("="*80)
print("LISTERIA MONOCYTOGENES DETECTION")
print("="*80)

# Count Lm test results
lm_results = Counter([r['lm_listeria_analysis'] for r in primary_data
                     if r['lm_listeria_analysis'] not in [None, 'NULL', '']])

print(f"\nListeria monocytogenes Test Results:")
total_lm_tested = sum(lm_results.values())
for result, count in lm_results.most_common():
    pct = (count / total_lm_tested) * 100
    print(f"  {result:50s}: {count:6,} ({pct:6.2f}%)")

# Calculate positive rate
lm_positive = sum(1 for r in primary_data if r['lm_listeria_analysis'] == 'Positive')
lm_positive_rate = (lm_positive / total_lm_tested * 100) if total_lm_tested > 0 else 0

print(f"\n** Listeria monocytogenes Positive Rate: {lm_positive_rate:.2f}% **")
print(f"   ({lm_positive:,} positives out of {total_lm_tested:,} tests)")


# ============================================================================
# CELL 10: Pathogen Detection Results - Salmonella
# ============================================================================

print("="*80)
print("SALMONELLA DETECTION")
print("="*80)

# Count Salmonella test results
sal_results = Counter([r['salmonella_sp_analysis'] for r in primary_data
                      if r['salmonella_sp_analysis'] not in [None, 'NULL', '']])

print(f"\nSalmonella Test Results:")
total_sal_tested = sum(sal_results.values())
for result, count in sal_results.most_common():
    pct = (count / total_sal_tested) * 100
    print(f"  {result:50s}: {count:6,} ({pct:6.2f}%)")

# Calculate positive rate
sal_positive = sum(1 for r in primary_data if r['salmonella_sp_analysis'] == 'Positive')
sal_positive_rate = (sal_positive / total_sal_tested * 100) if total_sal_tested > 0 else 0

print(f"\n** Salmonella Positive Rate: {sal_positive_rate:.2f}% **")
print(f"   ({sal_positive:,} positives out of {total_sal_tested:,} tests)")


# ============================================================================
# CELL 11: Sample Source Types
# ============================================================================

print("="*80)
print("SAMPLE SOURCE TYPES")
print("="*80)

sample_sources = Counter([r['sample_source_name'] for r in primary_data
                         if r['sample_source_name'] not in [None, 'NULL', '']])

print(f"\nTop 20 Sample Source Types:")
for source, count in sample_sources.most_common(20):
    pct = (count / len(primary_data)) * 100
    print(f"  {source[:70]:70s}: {count:5,} ({pct:5.2f}%)")

print(f"\nTotal unique sample source types: {len(sample_sources)}")


# ============================================================================
# CELL 12: Temporal Analysis - Date Range
# ============================================================================

print("="*80)
print("TEMPORAL ANALYSIS")
print("="*80)

dates = [r['collection_date'] for r in primary_data
         if r['collection_date'] not in [None, 'NULL', '']]

if dates:
    dates_sorted = sorted(dates)
    print(f"\nCollection Date Range:")
    print(f"  Earliest: {dates_sorted[0]}")
    print(f"  Latest: {dates_sorted[-1]}")
    print(f"  Total days covered: {(datetime.fromisoformat(dates_sorted[-1]) - datetime.fromisoformat(dates_sorted[0])).days}")
    print(f"  Samples with dates: {len(dates):,}")

# Count samples by month
from collections import defaultdict
samples_by_month = defaultdict(int)
for date_str in dates:
    month = date_str[:7]  # YYYY-MM
    samples_by_month[month] += 1

print(f"\nSamples by Month:")
for month in sorted(samples_by_month.keys()):
    count = samples_by_month[month]
    print(f"  {month}: {count:,} samples")


# ============================================================================
# CELL 13: Secondary Dataset - Genetic Characterization
# ============================================================================

print("="*80)
print("GENETIC CHARACTERIZATION - SECONDARY DATASET")
print("="*80)

print(f"\nTotal Secondary Records: {len(secondary_data):,}")
print("(These contain detailed pathogen characterization for positive samples)")

# Listeria allele codes (genetic fingerprints)
lm_alleles = Counter([r['lm_listeria_allele_code'] for r in secondary_data
                     if r['lm_listeria_allele_code'] not in [None, 'NULL', '']])

print(f"\n--- Listeria monocytogenes Genetic Data ---")
print(f"Unique allele codes (genetic fingerprints): {len(lm_alleles)}")
print(f"Total Lm characterizations: {sum(lm_alleles.values())}")

# Top 10 most common allele codes
print(f"\nTop 10 Most Common Allele Codes:")
for allele, count in lm_alleles.most_common(10):
    print(f"  {allele:30s}: {count:3,} occurrences")


# ============================================================================
# CELL 14: Listeria Sequence Types (MLST)
# ============================================================================

print("="*80)
print("LISTERIA SEQUENCE TYPES (MLST)")
print("="*80)

lm_mlst = Counter([r['lm_listeria_multi_locus_sequence'] for r in secondary_data
                  if r['lm_listeria_multi_locus_sequence'] not in [None, 'NULL', '']])

print(f"\nListeria monocytogenes Sequence Types:")
print(f"Total unique STs: {len(lm_mlst)}")
print(f"\nTop 15 Sequence Types:")
for st, count in lm_mlst.most_common(15):
    pct = (count / sum(lm_mlst.values())) * 100
    print(f"  {st:15s}: {count:3,} ({pct:5.2f}%)")


# ============================================================================
# CELL 15: Salmonella Serotypes
# ============================================================================

print("="*80)
print("SALMONELLA SEROTYPES")
print("="*80)

sal_serotypes = Counter([r['salmonella_serotype'] for r in secondary_data
                        if r['salmonella_serotype'] not in [None, 'NULL', '']])

print(f"\nSalmonella Serotypes Detected:")
print(f"Total unique serotypes: {len(sal_serotypes)}")
print(f"\nAll Serotypes:")
for serotype, count in sal_serotypes.most_common():
    print(f"  {serotype:30s}: {count:,}")


# ============================================================================
# CELL 16: Data Type Analysis
# ============================================================================

print("="*80)
print("DATA TYPE ANALYSIS")
print("="*80)

def infer_type(value):
    """Infer the data type of a value"""
    if value is None or value == "NULL" or value == "":
        return "NULL/Empty"
    if isinstance(value, bool):
        return "Boolean"
    if isinstance(value, int):
        return "Integer"
    if isinstance(value, float):
        return "Float"
    if isinstance(value, str):
        # Try to detect if it's a date
        if len(value) == 10 and value.count('-') == 2:
            return "Date (YYYY-MM-DD)"
        # Try to detect numeric strings
        try:
            float(value)
            return "Numeric String"
        except:
            pass
        return "String"
    return "Unknown"

# Analyze types for each column
column_types = defaultdict(lambda: defaultdict(int))
sample_values = defaultdict(set)

# Sample first 1000 records for type analysis
for record in primary_data[:1000]:
    for key, value in record.items():
        dtype = infer_type(value)
        column_types[key][dtype] += 1
        if dtype not in ["NULL/Empty"] and len(sample_values[key]) < 5:
            sample_values[key].add(str(value))

print("\nColumn Data Types (Primary Dataset):")
print(f"{'Column Name':<45} {'Primary Type':<20} {'Sample Values'}")
print("-" * 110)

for col in primary_data[0].keys():
    types = column_types[col]
    # Get the most common non-null type
    non_null_types = {k: v for k, v in types.items() if k != "NULL/Empty"}
    if non_null_types:
        primary_type = max(non_null_types.items(), key=lambda x: x[1])[0]
    else:
        primary_type = "NULL/Empty"

    samples = ", ".join(list(sample_values[col])[:3])
    if len(samples) > 40:
        samples = samples[:40] + "..."

    print(f"{col:<45} {primary_type:<20} {samples}")


# ============================================================================
# CELL 17: Positive Cases by State
# ============================================================================

print("="*80)
print("POSITIVE CASES BY STATE")
print("="*80)

# Count positive Listeria cases by state
lm_positive_by_state = defaultdict(int)
total_tests_by_state = defaultdict(int)

for record in primary_data:
    state = record['establishment_state']
    lm_result = record['lm_listeria_analysis']

    if state not in [None, 'NULL', ''] and lm_result not in [None, 'NULL', '']:
        total_tests_by_state[state] += 1
        if lm_result == 'Positive':
            lm_positive_by_state[state] += 1

# Calculate positive rates
state_positive_rates = {}
for state in total_tests_by_state:
    positives = lm_positive_by_state.get(state, 0)
    total = total_tests_by_state[state]
    rate = (positives / total * 100) if total > 0 else 0
    state_positive_rates[state] = (positives, total, rate)

# Sort by positive rate
print("\nStates with Listeria Positives (sorted by positive rate):")
print(f"{'State':<6} {'Positives':>10} {'Total Tests':>12} {'Positive Rate':>15}")
print("-" * 50)
for state, (positives, total, rate) in sorted(state_positive_rates.items(),
                                               key=lambda x: x[1][2], reverse=True):
    if positives > 0:  # Only show states with positives
        print(f"{state:<6} {positives:>10,} {total:>12,} {rate:>14.2f}%")


# ============================================================================
# CELL 18: Positive Cases by Establishment
# ============================================================================

print("="*80)
print("ESTABLISHMENTS WITH POSITIVE RESULTS")
print("="*80)

# Count positive results per establishment
establishment_positives = defaultdict(lambda: {'positives': 0, 'total': 0,
                                               'name': '', 'state': ''})

for record in primary_data:
    est_id = record['establishment_id']
    lm_result = record['lm_listeria_analysis']

    if est_id not in [None, 'NULL', ''] and lm_result not in [None, 'NULL', '']:
        establishment_positives[est_id]['total'] += 1
        establishment_positives[est_id]['name'] = record['establishment_name']
        establishment_positives[est_id]['state'] = record['establishment_state']
        if lm_result == 'Positive':
            establishment_positives[est_id]['positives'] += 1

# Find establishments with multiple positives
repeat_offenders = {k: v for k, v in establishment_positives.items()
                   if v['positives'] >= 2}

print(f"\nEstablishments with 2+ Positive Results: {len(repeat_offenders)}")
print(f"\n{'Est ID':<10} {'State':<6} {'Positives':>10} {'Total':>10} {'Rate':>10} {'Name':<40}")
print("-" * 95)

for est_id, data in sorted(repeat_offenders.items(),
                           key=lambda x: x[1]['positives'], reverse=True):
    rate = (data['positives'] / data['total'] * 100) if data['total'] > 0 else 0
    name = data['name'][:40]
    print(f"{est_id:<10} {data['state']:<6} {data['positives']:>10} "
          f"{data['total']:>10} {rate:>9.1f}% {name:<40}")


# ============================================================================
# CELL 19: Summary Statistics Report
# ============================================================================

print("="*80)
print("SUMMARY STATISTICS REPORT")
print("="*80)

print(f"""
DATASET OVERVIEW
----------------
Primary Records:              {len(primary_data):>10,}
Secondary Records:            {len(secondary_data):>10,}
Unique Establishments:        {unique_establishments:>10,}
States/Territories:           {unique_states:>10}

TEMPORAL COVERAGE
-----------------
Date Range:                   {dates_sorted[0]} to {dates_sorted[-1]}
Days Covered:                 {(datetime.fromisoformat(dates_sorted[-1]) - datetime.fromisoformat(dates_sorted[0])).days:>10}

PATHOGEN DETECTION
------------------
Listeria monocytogenes:
  Tests Performed:            {total_lm_tested:>10,}
  Positive Results:           {lm_positive:>10,}
  Positive Rate:              {lm_positive_rate:>9.2f}%

Salmonella:
  Tests Performed:            {total_sal_tested:>10,}
  Positive Results:           {sal_positive:>10,}
  Positive Rate:              {sal_positive_rate:>9.2f}%

GENETIC DIVERSITY
-----------------
Unique Lm Allele Codes:       {len(lm_alleles):>10}
Unique Lm Sequence Types:     {len(lm_mlst):>10}
Unique Salmonella Serotypes:  {len(sal_serotypes):>10}

GEOGRAPHIC CONCENTRATION
------------------------
Top 3 States:
  1. {states.most_common(3)[0][0]}: {states.most_common(3)[0][1]:,} samples
  2. {states.most_common(3)[1][0]}: {states.most_common(3)[1][1]:,} samples
  3. {states.most_common(3)[2][0]}: {states.most_common(3)[2][1]:,} samples

FACILITY RISK
-------------
Establishments with 2+ positives: {len(repeat_offenders):>6}
""")

print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
