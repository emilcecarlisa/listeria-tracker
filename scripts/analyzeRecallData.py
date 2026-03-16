#!/usr/bin/env python3
"""
Analyze FSIS Recall Summary data from 2025
Focuses on comparing animal vs plant-based product recalls
"""

try:
    import pandas as pd
    import openpyxl
    from datetime import datetime
    import warnings
    warnings.filterwarnings('ignore')

    print("=" * 80)
    print("FSIS RECALL SUMMARY 2025 ANALYSIS")
    print("=" * 80)

    # Load the Excel file
    print("\nLoading data from fsisRecallSummary2025.xlsx...")

    # First, peek at the file structure to handle any header rows
    df_raw = pd.read_excel('data/fsisRecallSummary2025.xlsx')

    print(f"\nRaw file preview (first 5 rows):")
    print(df_raw.head())

    # Check if there are metadata rows like in GCP files
    print(f"\nColumn headers detected: {df_raw.columns.tolist()}")

    # This appears to be a summary format file, not a detailed recall list
    # Check all sheets in the workbook
    print("\nChecking for multiple sheets...")
    xl_file = pd.ExcelFile('data/fsisRecallSummary2025.xlsx')
    print(f"Available sheets: {xl_file.sheet_names}")

    # Try to read each sheet
    df = None
    for sheet_name in xl_file.sheet_names:
        print(f"\nReading sheet: {sheet_name}")
        try:
            df_sheet = pd.read_excel('data/fsisRecallSummary2025.xlsx', sheet_name=sheet_name)
            print(f"  Shape: {df_sheet.shape}")
            print(f"  Columns: {df_sheet.columns.tolist()}")
            print(f"  First few rows:")
            print(df_sheet.head())

            # Use the sheet with the most columns and rows as main data
            if df is None or (df_sheet.shape[0] > df.shape[0] and df_sheet.shape[1] > 2):
                df = df_sheet
                print(f"  ✓ Using this sheet as primary data")
        except Exception as e:
            print(f"  Error reading sheet: {e}")

    if df is None:
        df = df_raw

    print('\n' + '='*80)
    print('DATA OVERVIEW')
    print('='*80)
    print(f'Total recall records: {len(df):,}')
    print(f'Date range: {df.shape[0]} records')

    print('\n' + '='*80)
    print('COLUMN STRUCTURE')
    print('='*80)
    print('\nColumn names:')
    for i, col in enumerate(df.columns, 1):
        print(f'  {i:2d}. {col}')

    print('\n' + '='*80)
    print('SAMPLE DATA')
    print('='*80)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 60)
    print(df.head(10))

    print('\n' + '='*80)
    print('DATA TYPES AND NON-NULL COUNTS')
    print('='*80)
    print(df.info())

    # Identify product type columns
    print('\n' + '='*80)
    print('IDENTIFYING PRODUCT CATEGORIES')
    print('='*80)

    product_cols = [col for col in df.columns if any(term in col.lower()
                    for term in ['product', 'item', 'food', 'type', 'category', 'name', 'description'])]
    print(f"\nProduct-related columns found: {product_cols}")

    # Search for animal vs plant keywords
    print('\n' + '='*80)
    print('ANIMAL VS PLANT PRODUCT CLASSIFICATION')
    print('='*80)

    # Animal product keywords
    animal_keywords = ['beef', 'pork', 'chicken', 'poultry', 'turkey', 'meat', 'sausage',
                       'bacon', 'ham', 'salami', 'pepperoni', 'hot dog', 'frankfurter',
                       'deli', 'steak', 'ground', 'patty', 'lamb', 'veal', 'duck', 'egg']

    # Plant product keywords
    plant_keywords = ['vegetable', 'fruit', 'lettuce', 'spinach', 'tomato', 'onion',
                      'grain', 'bread', 'pasta', 'rice', 'bean', 'salad', 'vegan',
                      'plant-based', 'veggie', 'herb', 'spice', 'nut', 'seed']

    # Ready-to-eat keywords
    rte_keywords = ['ready-to-eat', 'rte', 'pre-cooked', 'fully cooked', 'deli',
                    'prepared', 'ready to eat', 'cooked']

    # Raw keywords
    raw_keywords = ['raw', 'fresh', 'uncooked', 'ground']

    # Analyze each product column for classifications
    for col in product_cols:
        if col in df.columns:
            print(f"\n--- Analyzing column: {col} ---")

            # Count animal products
            animal_mask = df[col].astype(str).str.lower().str.contains('|'.join(animal_keywords), na=False)
            animal_count = animal_mask.sum()

            # Count plant products
            plant_mask = df[col].astype(str).str.lower().str.contains('|'.join(plant_keywords), na=False)
            plant_count = plant_mask.sum()

            # Count RTE products
            rte_mask = df[col].astype(str).str.lower().str.contains('|'.join(rte_keywords), na=False)
            rte_count = rte_mask.sum()

            # Count raw products
            raw_mask = df[col].astype(str).str.lower().str.contains('|'.join(raw_keywords), na=False)
            raw_count = raw_mask.sum()

            print(f"  Animal products: {animal_count:,} ({animal_count/len(df)*100:.1f}%)")
            print(f"  Plant products: {plant_count:,} ({plant_count/len(df)*100:.1f}%)")
            print(f"  Ready-to-eat: {rte_count:,} ({rte_count/len(df)*100:.1f}%)")
            print(f"  Raw products: {raw_count:,} ({raw_count/len(df)*100:.1f}%)")

            # Cross-tabulation: Animal RTE vs Animal Raw vs Plant RTE vs Plant Raw
            animal_rte = (animal_mask & rte_mask).sum()
            animal_raw = (animal_mask & raw_mask).sum()
            animal_neither = (animal_mask & ~rte_mask & ~raw_mask).sum()

            plant_rte = (plant_mask & rte_mask).sum()
            plant_raw = (plant_mask & raw_mask).sum()
            plant_neither = (plant_mask & ~rte_mask & ~raw_mask).sum()

            neither = (~animal_mask & ~plant_mask).sum()

            print(f"\n  Cross-classification:")
            print(f"    Animal RTE: {animal_rte:,}")
            print(f"    Animal Raw: {animal_raw:,}")
            print(f"    Animal (unclassified): {animal_neither:,}")
            print(f"    Plant RTE: {plant_rte:,}")
            print(f"    Plant Raw: {plant_raw:,}")
            print(f"    Plant (unclassified): {plant_neither:,}")
            print(f"    Neither animal nor plant detected: {neither:,}")

    # Identify reason/hazard columns
    print('\n' + '='*80)
    print('RECALL REASONS/HAZARDS')
    print('='*80)

    reason_cols = [col for col in df.columns if any(term in col.lower()
                   for term in ['reason', 'hazard', 'problem', 'issue', 'concern', 'pathogen'])]
    print(f"\nReason-related columns: {reason_cols}")

    for col in reason_cols:
        if col in df.columns:
            print(f"\n--- {col} ---")
            print(df[col].value_counts().head(10))

    # Look for listeria specifically
    print('\n' + '='*80)
    print('PATHOGEN-SPECIFIC ANALYSIS')
    print('='*80)

    pathogens = ['listeria', 'salmonella', 'e. coli', 'e.coli', 'campylobacter',
                 'clostridium', 'botulism']

    for pathogen in pathogens:
        count = 0
        for col in df.columns:
            matches = df[col].astype(str).str.contains(pathogen, case=False, na=False).sum()
            if matches > 0:
                count += matches
                print(f"  {pathogen.title()}: {matches} mentions in '{col}'")
        if count > 0:
            print(f"  Total {pathogen.title()} recalls: {count}")

    # Date analysis if date columns exist
    print('\n' + '='*80)
    print('TEMPORAL ANALYSIS')
    print('='*80)

    date_cols = [col for col in df.columns if any(term in col.lower()
                 for term in ['date', 'time', 'year', 'month'])]
    print(f"\nDate-related columns: {date_cols}")

    for col in date_cols:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                if df[col].notna().sum() > 0:
                    print(f"\n{col}:")
                    print(f"  Earliest: {df[col].min()}")
                    print(f"  Latest: {df[col].max()}")
                    print(f"  Valid dates: {df[col].notna().sum()}")
            except:
                print(f"\n{col}: Unable to parse as dates")

    print('\n' + '='*80)
    print('SUMMARY STATISTICS')
    print('='*80)

    # Try to generate summary if we have identified columns
    if product_cols:
        main_product_col = product_cols[0]
        print(f"\nUsing '{main_product_col}' for summary:")
        print(f"  Total recalls: {len(df):,}")

        animal_mask = df[main_product_col].astype(str).str.lower().str.contains('|'.join(animal_keywords), na=False)
        plant_mask = df[main_product_col].astype(str).str.lower().str.contains('|'.join(plant_keywords), na=False)

        print(f"  Animal product recalls: {animal_mask.sum():,} ({animal_mask.sum()/len(df)*100:.1f}%)")
        print(f"  Plant product recalls: {plant_mask.sum():,} ({plant_mask.sum()/len(df)*100:.1f}%)")
        print(f"  Other/Unclassified: {(~animal_mask & ~plant_mask).sum():,}")

    print('\n' + '='*80)
    print('EXPORTING ENRICHED DATA')
    print('='*80)

    # Add classification columns if we have product data
    if product_cols and len(product_cols) > 0:
        main_col = product_cols[0]
        df['is_animal_product'] = df[main_col].astype(str).str.lower().str.contains('|'.join(animal_keywords), na=False)
        df['is_plant_product'] = df[main_col].astype(str).str.lower().str.contains('|'.join(plant_keywords), na=False)
        df['is_rte'] = df[main_col].astype(str).str.lower().str.contains('|'.join(rte_keywords), na=False)
        df['is_raw'] = df[main_col].astype(str).str.lower().str.contains('|'.join(raw_keywords), na=False)

        # Save enriched data
        output_file = 'data/recallDataEnriched.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✓ Enriched recall data saved to: {output_file}")

    print('\n' + '='*80)
    print('ANALYSIS COMPLETE')
    print('='*80)

    print("\nNext steps:")
    print("  1. Review the output above to understand the data structure")
    print("  2. Create detailed analysis document based on findings")
    print("  3. Generate visualizations for dashboard")

except ImportError as e:
    print(f"Error: Required module not found - {e}")
    print("Please install required packages: pip install pandas openpyxl")
except FileNotFoundError as e:
    print(f"Error: File not found - {e}")
    print("Please ensure fsisRecallSummary2025.xlsx exists in the data/ directory")
except Exception as e:
    print(f"Error analyzing data: {e}")
    import traceback
    traceback.print_exc()
