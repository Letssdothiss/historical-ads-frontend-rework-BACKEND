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
    
    

