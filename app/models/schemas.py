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
# Search parameters schema
class SearchParams(BaseModel):
    """Search parameters schema"""
    q: Optional[str] = Field(None, description="Free text search query")
    offset: int = Field(0, ge=0, description="Result offset for pagination")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")
    published_before: Optional[str] = Field(None, description="Filter ads published before date (YYYY-MM-DD)")
    published_after: Optional[str] = Field(None, description="Filter ads published after date (YYYY-MM-DD)")
    occupation: Optional[List[str]] = Field(None, description="Filter by occupation concept IDs")
    occupation_group: Optional[List[str]] = Field(None, description="Filter by occupation group IDs")
    occupation_field: Optional[List[str]] = Field(None, description="Filter by occupation field IDs")
    municipality: Optional[List[str]] = Field(None, description="Filter by municipality")
    region: Optional[List[str]] = Field(None, description="Filter by region")
    country: Optional[List[str]] = Field(None, description="Filter by country")
    employment_type: Optional[List[str]] = Field(None, description="Filter by employment type")
    experience_required: Optional[bool] = Field(None, description="Filter by experience required")
    