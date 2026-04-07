#!/usr/bin/env python3
"""
Prepare all data for comprehensive dashboard
Backend processing - generates cleaned datasets
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA_PATH = Path('../data')
OUTPUT_PATH = Path('../data/processed')
OUTPUT_PATH.mkdir(exist_ok=True)

print("="*80)
print("DATA PREPARATION FOR DASHBOARD")
print("="*80)

# 1. Load and clean consumption data
print("\n1. Processing consumption data...")
consumption_df = pd.read_csv(DATA_PATH / 'usFoodGroupIntakesBySource.csv')

consumption_recent = consumption_df[
    (consumption_df['Survey years:Variable'] == '2017-2018-Mean') &
    (consumption_df['Demographics'] == 'US consumers aged 2 and above') &
    (consumption_df['Food group'] != 'Energy')
].copy()

def convertToOunces(row):
    if row['Measurement'] == 'Ounces':
        return row['Value']
    elif row['Measurement'] == 'Cups':
        return row['Value'] * 8
    elif row['Measurement'] == 'Grams':
        return row['Value'] / 28.35
    elif row['Measurement'] == 'Teaspoons':
        return row['Value'] * 0.166667
    return 0

consumption_recent['ozEquivalent'] = consumption_recent.apply(convertToOunces, axis=1)

animalKeywords = ['meat', 'poultry', 'eggs', 'seafood', 'fish', 'dairy', 'cured']
plantKeywords = ['vegetable', 'fruit', 'grain', 'legume', 'nut', 'seed', 'soy']

def categorizeFoodSource(foodGroup):
    if pd.isna(foodGroup):
        return 'Other'
    foodLower = str(foodGroup).lower()
    for keyword in animalKeywords:
        if keyword in foodLower:
            return 'Animal'
    for keyword in plantKeywords:
        if keyword in foodLower:
            return 'Plant'
    return 'Other'

consumption_recent['foodType'] = consumption_recent['Food group'].apply(categorizeFoodSource)
consumption_recent.to_csv(OUTPUT_PATH / 'consumptionCleaned.csv', index=False)
print(f"✓ Consumption data: {len(consumption_recent)} records")

# 2. Load joined GCP+Lab data
print("\n2. Processing GCP+Lab data...")
joinedData = pd.read_csv(DATA_PATH / 'joinedGcpLabPoultryData.csv')
bothData = joinedData[joinedData['_merge'] == 'both'].copy()
bothData.to_csv(OUTPUT_PATH / 'gcpLabJoined.csv', index=False)
print(f"✓ GCP+Lab data: {len(bothData)} establishments")

# 3. Load NEW recall data
print("\n3. Processing recall data...")
recallsDf = pd.read_csv(DATA_PATH / 'recallsAllCombined.csv')

# Derive pathogen from summary text
def categorizePathogen(row):
    text = str(row['summary']).lower() + ' ' + str(row['title']).lower()
    if 'listeria' in text:
        return 'Listeria'
    elif 'salmonella' in text:
        return 'Salmonella'
    return 'Unknown'

recallsDf['pathogen'] = recallsDf.apply(categorizePathogen, axis=1)

# Convert dates
recallsDf['recallDate'] = pd.to_datetime(recallsDf['recallDate'], errors='coerce')
recallsDf['closedDate'] = pd.to_datetime(recallsDf['closedDate'], errors='coerce')
recallsDf['daysOpen'] = (recallsDf['closedDate'] - recallsDf['recallDate']).dt.days

# Filter for FY2025 alignment (Oct 1, 2024 - Sep 30, 2025)
fy2025_start = pd.to_datetime('2024-10-01')
fy2025_end = pd.to_datetime('2025-09-30')
recallsDf['inFY2025'] = (recallsDf['recallDate'] >= fy2025_start) & (recallsDf['recallDate'] <= fy2025_end)

# Export full dataset
recallsDf.to_csv(OUTPUT_PATH / 'recallsApi.csv', index=False)
print(f"✓ Recall data (API): {len(recallsDf)} recalls")
print(f"  Listeria: {(recallsDf['pathogen'] == 'Listeria').sum()}")
print(f"  Salmonella: {(recallsDf['pathogen'] == 'Salmonella').sum()}")
print(f"  Total pounds: {recallsDf['poundsRecovered'].sum():,.0f}")

# Export FY2025-aligned subset
recallsDf_fy2025 = recallsDf[recallsDf['inFY2025']].copy()
recallsDf_fy2025.to_csv(OUTPUT_PATH / 'recallsApiFY2025.csv', index=False)
print(f"\n✓ Temporal Alignment:")
print(f"  Lab data period: FY2025 (Oct 2024 - Sep 2025)")
print(f"  Recalls in FY2025: {len(recallsDf_fy2025)} of {len(recallsDf)} ({len(recallsDf_fy2025)/len(recallsDf)*100:.1f}%)")
print(f"  Recalls outside period: {len(recallsDf) - len(recallsDf_fy2025)} (context only)")

# 4. Create establishment lookup
print("\n4. Creating establishment cross-reference...")
recallEstablishments = recallsDf.groupby('establishment').agg({
    'recallNumber': 'count',
    'poundsRecovered': 'sum',
    'relatedToOutbreak': 'sum',
    'pathogen': lambda x: ', '.join(x.unique())
}).reset_index()

recallEstablishments.columns = ['establishment', 'recallCount', 'totalPounds', 'outbreakCount', 'pathogens']
recallEstablishments.to_csv(OUTPUT_PATH / 'recallsByEstablishment.csv', index=False)
print(f"✓ Establishments with recalls: {len(recallEstablishments)}")

# 5. Calculate summary statistics
print("\n5. Calculating summary statistics...")
stats = {
    # Contamination
    'totalSamples': int(bothData['Lab_TotalSamples'].sum()),
    'totalPositive': int(bothData['Lab_SalmonellaPositive'].sum()),
    'overallRate': float(bothData['Lab_SalmonellaPositive'].sum() / bothData['Lab_TotalSamples'].sum() * 100),

    # Welfare
    'totalEstablishments': int(len(bothData)),
    'withMOIs': int((bothData['GCP_TotalMOIs'] > 0).sum()),
    'withNRs': int((bothData['GCP_TotalNRs'] > 0).sum()),
    'moiPercent': float((bothData['GCP_TotalMOIs'] > 0).sum() / len(bothData) * 100),

    # Recalls (all data)
    'totalRecalls': int(len(recallsDf)),
    'listeriaRecalls': int((recallsDf['pathogen'] == 'Listeria').sum()),
    'salmonellaRecalls': int((recallsDf['pathogen'] == 'Salmonella').sum()),
    'outbreakRecalls': int(recallsDf['relatedToOutbreak'].sum()),
    'totalPoundsRecalled': float(recallsDf['poundsRecovered'].sum()),
    'largestRecall': {
        'establishment': recallsDf.loc[recallsDf['poundsRecovered'].idxmax(), 'establishment'],
        'pounds': float(recallsDf['poundsRecovered'].max()),
        'pathogen': recallsDf.loc[recallsDf['poundsRecovered'].idxmax(), 'pathogen']
    },
    'top5Recalls': recallsDf.nlargest(5, 'poundsRecovered')[['establishment', 'poundsRecovered', 'pathogen', 'relatedToOutbreak']].to_dict('records'),

    # Temporal alignment
    'recallsFY2025': int(len(recallsDf_fy2025)),
    'recallsOutsideFY2025': int(len(recallsDf) - len(recallsDf_fy2025)),
    'alignmentPercent': float(len(recallsDf_fy2025) / len(recallsDf) * 100) if len(recallsDf) > 0 else 0,
    'fy2025Period': 'Oct 1, 2024 - Sep 30, 2025'
}

with open(OUTPUT_PATH / 'dashboardStats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("✓ Summary statistics calculated")

print("\n" + "="*80)
print("DATA PREPARATION COMPLETE")
print("="*80)
print("\nGenerated Files:")
print(f"  • consumptionCleaned.csv")
print(f"  • gcpLabJoined.csv")
print(f"  • recallsApi.csv (all recalls)")
print(f"  • recallsApiFY2025.csv (FY2025-aligned only)")
print(f"  • recallsByEstablishment.csv")
print(f"  • dashboardStats.json")
print("\nKey Statistics:")
print(f"  Contamination rate: {stats['overallRate']:.2f}%")
print(f"  Welfare concerns: {stats['moiPercent']:.1f}%")
print(f"  Total recalls: {stats['totalRecalls']}")
print(f"    FY2025-aligned: {stats['recallsFY2025']} ({stats['alignmentPercent']:.1f}%)")
print(f"    Context only: {stats['recallsOutsideFY2025']}")
print(f"  Total pounds recalled: {stats['totalPoundsRecalled']:,.0f}")
print(f"  Largest recall: {stats['largestRecall']['establishment']} ({stats['largestRecall']['pounds']:,.0f} lbs)")
print("\n✓ Ready for dashboard visualization")
