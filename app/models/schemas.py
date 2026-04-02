"""Request/Response schemas"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ExportFormat(str, Enum):
    """Export format enum"""

    JSON = "json"
    CSV = "csv"
    XLSX = "xlsx"


class SearchQuery(BaseModel):
    """Search query parameters"""

    q: Optional[str] = Field(None, description="Free text search")
    offset: int = Field(0, ge=0, description="Pagination offset")
    limit: int = Field(10, ge=1, le=100, description="Number of results")
    published_before: Optional[str] = Field(None, description="Before date YYYY-MM-DD")
    published_after: Optional[str] = Field(None, description="After date YYYY-MM-DD")
    occupation: Optional[List[str]] = Field(None, description="Occupation IDs")
    occupation_group: Optional[List[str]] = Field(None, description="Occupation group IDs")
    occupation_field: Optional[List[str]] = Field(None, description="Occupation field IDs")
    municipality: Optional[List[str]] = Field(None, description="Municipality IDs")
    region: Optional[List[str]] = Field(None, description="Region IDs")
    country: Optional[List[str]] = Field(None, description="Country IDs")
    employment_type: Optional[List[str]] = Field(None, description="Employment type IDs")
    experience_required: Optional[bool] = Field(None, description="Experience required")


class ExportQuery(BaseModel):
    """Export query parameters"""

    search: SearchQuery = Field(default_factory=SearchQuery)
    format: ExportFormat = Field(ExportFormat.JSON, description="Export format")
    fields: Optional[List[str]] = Field(None, description="Fields to export")
