"""
Data storage utilities - Save and load recall data
"""

import json
import csv
from typing import List, Dict, Any
from pathlib import Path


class RecallStorage:
    """Storage manager for recall data"""

    @staticmethod
    def saveToJson(data: List[Dict[str, Any]], filepath: Path) -> None:
        """
        Save recall data to JSON file

        Args:
            data: List of recall records
            filepath: Output file path
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved {len(data)} records to: {filepath}")

    @staticmethod
    def saveToCsv(data: List[Dict[str, Any]], filepath: Path) -> None:
        """
        Save recall data to CSV file

        Args:
            data: List of recall records
            filepath: Output file path
        """
        if not data:
            print("⚠️  No data to save to CSV")
            return

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Get all unique keys from all records
        allKeys = set()
        for record in data:
            allKeys.update(record.keys())

        fieldnames = sorted(allKeys)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"✓ Saved {len(data)} records to: {filepath}")

    @staticmethod
    def loadFromJson(filepath: Path) -> List[Dict[str, Any]]:
        """
        Load recall data from JSON file

        Args:
            filepath: Input file path

        Returns:
            List of recall records
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✓ Loaded {len(data)} records from: {filepath}")
        return data

    @staticmethod
    def mergeDeduplicate(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge and deduplicate recall records by recall number

        For duplicate recall numbers, keep the expansion (EXP) version if it exists,
        otherwise keep the record with the most data.

        Args:
            records: List of recall records

        Returns:
            Deduplicated list
        """
        # Group by recall number (without -EXP suffix)
        grouped = {}

        for record in records:
            recallNum = record.get('recallNumber', '')
            baseNum = recallNum.replace('-EXP', '')

            if baseNum not in grouped:
                grouped[baseNum] = []

            grouped[baseNum].append(record)

        # For each group, pick the best record
        deduplicated = []

        for baseNum, group in grouped.items():
            if len(group) == 1:
                deduplicated.append(group[0])
            else:
                # Prefer EXP version
                expRecords = [r for r in group if '-EXP' in r.get('recallNumber', '')]
                if expRecords:
                    # Use the EXP version
                    deduplicated.append(expRecords[0])
                else:
                    # Use the one with the most non-empty fields
                    best = max(group, key=lambda r: sum(1 for v in r.values() if v))
                    deduplicated.append(best)

        return deduplicated
