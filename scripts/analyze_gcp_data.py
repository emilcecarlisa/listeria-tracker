#!/usr/bin/env python3
"""
Analyze the GCP (Good Commercial Practices) archive data from FY2024
"""

try:
    import pandas as pd
    import openpyxl
    from datetime import datetime

    # Load the Excel file
    print("Loading data from 0post-GCP_arch24.xlsx...")
    df = pd.read_excel('data/0post-GCP_arch24.xlsx')

    print('\n' + '='*60)
    print('DATA OVERVIEW')
    print('='*60)
    print(f'Total records: {len(df):,}')

    print('\nColumn names:')
    for i, col in enumerate(df.columns, 1):
        print(f'  {i:2d}. {col}')

    # Count violations (records with NR - Noncompliance Records)
    # We need to identify which columns contain NR information
    print('\n' + '='*60)
    print('SEARCHING FOR VIOLATION/NONCOMPLIANCE INDICATORS')
    print('='*60)

    # Check for columns that might contain NR or violation information
    nr_related_cols = [col for col in df.columns if any(term in col.lower() for term in ['nr', 'noncompliance', 'violation', 'regulation', 'description'])]
    print(f'\nFound {len(nr_related_cols)} potential NR-related columns:')
    for col in nr_related_cols:
        print(f'  - {col}')

    # Display sample data
    print('\n' + '='*60)
    print('SAMPLE DATA (first 3 rows)')
    print('='*60)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df.head(3))

    # Search for George's Foods incident in April 2024
    print('\n' + '='*60)
    print('SEARCHING FOR GEORGES FOODS (P2186) APRIL 2024 INCIDENT')
    print('='*60)

    # Look for establishment number P2186
    est_cols = [col for col in df.columns if 'establishment' in col.lower() or 'est' in col.lower()]
    print(f'\nEstablishment-related columns: {est_cols}')

    # Try to find records with P2186
    for col in df.columns:
        if df[col].astype(str).str.contains('2186|P2186', case=False, na=False).any():
            print(f'\nFound "2186" or "P2186" in column: {col}')
            matches = df[df[col].astype(str).str.contains('2186|P2186', case=False, na=False)]
            print(f'Number of matching records: {len(matches)}')

    # Look for April 2024 records
    date_cols = [col for col in df.columns if any(term in col.lower() for term in ['date', 'time', 'inspection'])]
    print(f'\nDate-related columns: {date_cols}')

    # Try to find records from April 2024
    for col in date_cols:
        try:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                april_2024 = df[(df[col].dt.year == 2024) & (df[col].dt.month == 4)]
                if len(april_2024) > 0:
                    print(f'\nFound {len(april_2024)} records from April 2024 in column: {col}')
        except:
            # Try string search for date patterns
            if df[col].astype(str).str.contains('4/12/2024|04/12/2024|2024-04-12|Apr.*2024|April.*2024', case=False, na=False).any():
                print(f'\nFound date pattern in column: {col}')

    # Search for keywords from the incident description
    print('\n' + '='*60)
    print('SEARCHING FOR INCIDENT KEYWORDS')
    print('='*60)
    keywords = ['throw', 'thrown', 'chicken', 'wall', 'respiratory distress', 'mistreatment', 'George']

    for keyword in keywords:
        for col in df.columns:
            if df[col].astype(str).str.contains(keyword, case=False, na=False).any():
                matches = df[df[col].astype(str).str.contains(keyword, case=False, na=False)]
                print(f'\nKeyword "{keyword}" found in column "{col}": {len(matches)} match(es)')
                if len(matches) <= 5:
                    print(f'  Matching values:')
                    for idx, val in matches[col].head().items():
                        print(f'    Row {idx}: {str(val)[:100]}...' if len(str(val)) > 100 else f'    Row {idx}: {val}')

    # Count total violations (assuming NR fields indicate violations)
    print('\n' + '='*60)
    print('VIOLATION COUNTS')
    print('='*60)

    # Try to count violations based on NR-related fields
    if nr_related_cols:
        for col in nr_related_cols:
            non_null_count = df[col].notna().sum()
            if non_null_count > 0:
                print(f'\n{col}:')
                print(f'  Non-empty records: {non_null_count:,}')
                print(f'  Empty records: {(len(df) - non_null_count):,}')

    print('\n' + '='*60)
    print('ANALYSIS COMPLETE')
    print('='*60)

except ImportError as e:
    print(f"Error: Required module not found - {e}")
    print("Please install required packages: pip install pandas openpyxl")
except Exception as e:
    print(f"Error analyzing data: {e}")
    import traceback
    traceback.print_exc()
