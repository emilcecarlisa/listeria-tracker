"""
Recall data parsers - Extract and normalize fields from API responses
"""

from typing import Dict, Any, List, Optional
import re
from html import unescape


class RecallParser:
    """Parser for FSIS recall API responses"""

    @staticmethod
    def parseRecall(record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single recall record from API response

        Args:
            record: Raw recall record from API

        Returns:
            Normalized recall data
        """
        parsed = {
            # Core identifiers
            'recallNumber': record.get('field_recall_number', ''),
            'recallClass': record.get('field_recall_classification', ''),
            'riskLevel': record.get('field_risk_level', ''),

            # Company info
            'establishment': record.get('field_establishment', ''),
            'companyContact': RecallParser._cleanText(record.get('field_company_media_contact', '')),

            # Product info
            'title': record.get('field_title', ''),
            'productItems': RecallParser._cleanText(record.get('field_product_items', '')),
            'processingCategory': record.get('field_processing', ''),

            # Recall details
            'recallReason': record.get('field_recall_reason', ''),
            'recallType': record.get('field_recall_type', ''),
            'poundsRecovered': RecallParser._parsePounds(record.get('field_qty_recovered', '')),

            # Dates
            'recallDate': record.get('field_recall_date', ''),
            'closedDate': record.get('field_closed_date', ''),
            'closedYear': record.get('field_closed_year', ''),
            'year': record.get('field_year', ''),

            # Geographic
            'states': record.get('field_states', ''),

            # Outbreak
            'relatedToOutbreak': record.get('field_related_to_outbreak', 'False') == 'True',

            # Status
            'isArchived': record.get('field_archive_recall', 'False') == 'True',
            'isActive': record.get('field_active_notice', 'False') == 'True',

            # Additional
            'summary': RecallParser._cleanHtml(record.get('field_summary', '')),
            'recallUrl': record.get('field_recall_url', ''),
            'distributionList': record.get('field_distro_list', ''),
            'labels': record.get('field_labels', ''),

            # Language
            'language': record.get('langcode', 'English'),
            'hasSpanish': record.get('field_has_spanish', 'False') == 'True'
        }

        return parsed

    @staticmethod
    def _parsePounds(poundsStr: str) -> Optional[int]:
        """
        Extract numeric pounds from string like '60,020 lbs'

        Args:
            poundsStr: String containing pounds

        Returns:
            Numeric pounds or None
        """
        if not poundsStr:
            return None

        # Remove commas and extract digits
        match = re.search(r'([\d,]+)', poundsStr)
        if match:
            return int(match.group(1).replace(',', ''))

        return None

    @staticmethod
    def _cleanText(text: str) -> str:
        """
        Clean text by removing extra whitespace

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        if not text:
            return ''

        # Remove multiple spaces/newlines
        cleaned = re.sub(r'\s+', ' ', text)
        return cleaned.strip()

    @staticmethod
    def _cleanHtml(html: str) -> str:
        """
        Remove HTML tags and unescape entities

        Args:
            html: HTML string

        Returns:
            Plain text
        """
        if not html:
            return ''

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)

        # Unescape HTML entities
        text = unescape(text)

        # Clean whitespace
        text = RecallParser._cleanText(text)

        return text

    @staticmethod
    def parseMultiple(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse multiple recall records

        Args:
            records: List of raw recall records

        Returns:
            List of normalized recall data
        """
        return [RecallParser.parseRecall(record) for record in records]
