# Data schemas for the application
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
# Export format options
class ExportFormat(str, Enum):
    CSV = 'csv'
    JSON = 'json'
    XLSX = 'xlsx'
# Sorting options
class SortOrder(str, Enum):
    ASC = 'asc'
    DESC = 'desc'
