"""Data Processor for handling job ad data"""
import io
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

from app.utils.config import settings
# Logger for the DataProcessor class, used to log information and errors during data processing tasks.
logger = logging.getLogger(__name__)


class DataProcessor:
    """Data processor for handling job ad data"""
    DEFAULT_EXPORT_FIELDS = [
        "id",
        "original_id",
        "headline",
        "publication_date",
        "application_deadline",
        "number_of_vacancies",
        "employer.name",
        "workplace_address.municipality",
        "workplace_address.region",
        "occupation.label",
        "occupation_group.label",
        "occupation_field.label",
        "employment_type.label",
        "duration.label",
        "working_hours_type.label",
    ]
    @staticmethod
    def flatten_dict(
      d: Dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> Dict[str, Any]:
      """ Flatten a nested dictionary """
      items = []
      for k, v in d.items():
          new_key = f"{parent_key}{sep}{k}" if parent_key else k
          if isinstance(v, dict):
              items.extend(DataProcessor.flatten_dict(v, new_key, sep=sep).items())
          elif isinstance(v, list):
              if v and isinstance(v[0], dict):
                  items.append((new_key, json.dumps(v)))
              else:
                  items.append((new_key, ", ".join(str(x) for x in v)))
          else:
              items.append((new_key, v))
      return dict(items)

    @staticmethod
    def extract_fields(ad: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """Extract specified fields from a job ad"""
        flat_ad = DataProcessor.flatten_dict(ad)
        return {field: flat_ad.get(field, "") for field in fields}

    @staticmethod
    def process_search_results(
        results: Dict[str, Any], fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Process search results for cleaner output"""
        return {
            "total": results.get("total", {"value": 0}),
            "offset": results.get("offset", 0),
            "limit": results.get("limit", 10),
            "hits": results.get("hits", []),
            "took": results.get("took"),
            "freetext_concepts": results.get("freetext_concepts"),
        }

    @staticmethod
    def export_to_json(
        ads: List[Dict[str, Any]],
        fields: Optional[List[str]] = None,
        pretty: bool = True,
    ) -> str:
        """Export job ads as JSON"""
        if fields:
            ads = [DataProcessor.extract_fields(ad, fields) for ad in ads]
        indent = 2 if pretty else None
        return json.dumps(ads, indent=indent, ensure_ascii=False, default=str)

    @staticmethod
    def export_to_csv(
        ads: List[Dict[str, Any]],
        fields: Optional[List[str]] = None,
        delimiter: str = ",",
    ) -> str:
        """Export job ads as CSV"""
        if not ads:
            return ""

        fields = fields or DataProcessor.DEFAULT_EXPORT_FIELDS
        flat_ads = [DataProcessor.extract_fields(ad, fields) for ad in ads]
        df = pd.DataFrame(flat_ads)

        for field in fields:
            if field not in df.columns:
                df[field] = ""

        df = df[fields]
        return df.to_csv(index=False, sep=delimiter)

    @staticmethod
    def export_to_xlsx(
        ads: List[Dict[str, Any]],
        fields: Optional[List[str]] = None,
        sheet_name: str = "Historiska annonser",
    ) -> bytes:
        """Export job ads as Excel (XLSX)"""
        fields = fields or DataProcessor.DEFAULT_EXPORT_FIELDS

        if not ads:
            df = pd.DataFrame()
        else:
            flat_ads = [DataProcessor.extract_fields(ad, fields) for ad in ads]
            df = pd.DataFrame(flat_ads)

            for field in fields:
                if field not in df.columns:
                    df[field] = ""

            df = df[fields]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        return output.getvalue()

    @staticmethod
    def generate_filename(query: Optional[str] = None, format: str = "json") -> str:
        """Generate a filename for export"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if query:
            safe_query = "".join(
                c if c.isalnum() or c in (" ", "-", "_") else "" for c in query
            )
            safe_query = safe_query[:50].strip().replace(" ", "_")
            return f"historiska_annonser_{safe_query}_{timestamp}"

        return f"historiska_annonser_{timestamp}"

    @staticmethod
    def extract_filter_options(
        stats_data: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Extract filter options from stats data"""
        stats = stats_data.get("stats", {})

        return {
            "occupations": stats.get("occupation-name", [])[:20],
            "regions": stats.get("region", [])[:21],
            "municipalities": stats.get("municipality", [])[:50],
            "employment_types": stats.get("employment-type", []),
            "occupation_fields": stats.get("occupation-field", []),
        }


# Singleton instance
_data_processor: Optional[DataProcessor] = None


def get_data_processor() -> DataProcessor:
    """Get or create DataProcessor instance"""
    global _data_processor
    if _data_processor is None:
        _data_processor = DataProcessor()
    return _data_processor
