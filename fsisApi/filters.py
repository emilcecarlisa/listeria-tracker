"""
Filter builders for FSIS API queries
"""

from typing import Dict, Any, Optional


class RecallFilters:
    """Builder for FSIS API filter parameters"""

    # Year to taxonomy ID mapping (from API documentation Appendix A)
    YEAR_IDS = {
        2020: 1,
        2021: 446,
        2022: 444,
        2023: 445,
        2024: 606,
        2025: 684,
        2026: 685,
        2027: 686
    }

    @staticmethod
    def year(year: int) -> Dict[str, Any]:
        """
        Filter by issue year

        Args:
            year: Issue year (e.g., 2024, 2025)

        Returns:
            Filter parameters with taxonomy ID

        Raises:
            ValueError: If year not supported
        """
        if year not in RecallFilters.YEAR_IDS:
            raise ValueError(f"Year {year} not supported. Available years: {list(RecallFilters.YEAR_IDS.keys())}")

        return {'field_year_id': str(RecallFilters.YEAR_IDS[year])}

    @staticmethod
    def pathogen(pathogen: str) -> Dict[str, Any]:
        """
        Filter by pathogen in summary/product text

        Args:
            pathogen: Pathogen name (e.g., 'listeria', 'salmonella')

        Returns:
            Filter parameters
        """
        return {'field_summary_value': pathogen.lower()}

    @staticmethod
    def yearAndPathogen(year: int, pathogen: str) -> Dict[str, Any]:
        """
        Combine year and pathogen filters

        Args:
            year: Issue year
            pathogen: Pathogen name

        Returns:
            Combined filter parameters
        """
        filters = {}
        filters.update(RecallFilters.year(year))
        filters.update(RecallFilters.pathogen(pathogen))
        return filters

    @staticmethod
    def productType(product: str) -> Dict[str, Any]:
        """
        Filter by product type

        Args:
            product: Product type (e.g., 'meat', 'poultry')

        Returns:
            Filter parameters
        """
        return {'field_product_items_value': product.lower()}

    @staticmethod
    def recallClass(classNum: str) -> Dict[str, Any]:
        """
        Filter by recall class

        Args:
            classNum: Recall class ('I', 'II', or 'III')

        Returns:
            Filter parameters
        """
        return {'field_recall_classification_id': f"Class {classNum}"}

    @staticmethod
    def combine(**kwargs) -> Dict[str, Any]:
        """
        Combine multiple filters

        Args:
            **kwargs: Keyword arguments for different filters
                     (year, pathogen, product, recallClass)

        Returns:
            Combined filter parameters
        """
        filters = {}

        if 'year' in kwargs:
            filters.update(RecallFilters.year(kwargs['year']))

        if 'pathogen' in kwargs:
            filters.update(RecallFilters.pathogen(kwargs['pathogen']))

        if 'product' in kwargs:
            filters.update(RecallFilters.productType(kwargs['product']))

        if 'recallClass' in kwargs:
            filters.update(RecallFilters.recallClass(kwargs['recallClass']))

        return filters
