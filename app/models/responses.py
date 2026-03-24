# Response models for the API
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class JobAd(BaseModel):
  """ Job ad model """
  id: str = Field(..., description="Unique identifier for the ad")
  original_id: Optional[str] = Field(None, description="Original ad ID")
  headline: Optional[str] = Field(None, description="Job ad headline")
  description: Optional[Dict[str, Any]] = Field(None, description="Job description")
  employer: Optional[Dict[str, Any]] = Field(None, description="Employer information")
  workplace_address: Optional[Dict[str, Any]] = Field(None, description="Workplace address")
  occupation: Optional[Dict[str, Any]] = Field(None, description="Occupation details")
  occupation_group: Optional[Dict[str, Any]] = Field(None, description="Occupation group")
  occupation_field: Optional[Dict[str, Any]] = Field(None, description="Occupation field")
  employment_type: Optional[Dict[str, Any]] = Field(None, description="Employment type")
  duration: Optional[Dict[str, Any]] = Field(None, description="Employment duration")
  salary_type: Optional[Dict[str, Any]] = Field(None, description="Salary type")
  working_hours_type: Optional[Dict[str, Any]] = Field(None, description="Working hours type")
  publication_date: Optional[str] = Field(None, description="Publication date")
  application_deadline: Optional[str] = Field(None, description="Application deadline")
  number_of_vacancies: Optional[int] = Field(None, description="Number of vacancies")
  relevance: Optional[int] = Field(None, description="Search relevance score")

  # Allow additional fields not explicitly defined in the model.
  # Useful when the API may return extra data that we still want to accept.
class Config:
  extra = 'allow'

  # Represents the response returned from a job search query.
  # Contains pagination metadata and a list of matching JobAd objects.
class SearchResult(BaseModel):
  """Search result model"""
  total: Dict[str, Any] = Field(..., description="Total number of matching ads")
  offset: int = Field(..., description="Current offset")
  limit: int = Field(..., description="Current limit")
  hits: List[JobAd] = Field(default_factory=list, description="List of job ads")
  took: Optional[int] = Field(None, description="Query execution time in ms")
  freetext_concepts: Optional[Dict[str, Any]] = Field(None, description="Extracted concepts from search")
class Config:
  extra = 'allow'
  # Represents a single statistics entry returned from the API,
  # describing how often a specific concept or category occurs in search results.
class StatsItem(BaseModel):
    """Statistics item"""
    concept_id: Optional[str] = Field(None, description="Concept ID")
    label: str = Field(..., description="Display label")
    legacy_ams_taxonomy_id: Optional[str] = Field(None, description="Legacy taxonomy ID")
    occurrences: int = Field(..., description="Number of occurrences")
  # Represents the statistics response returned from the API.
  # Contains execution timing information and aggregated statistics
  # grouped by category, where each category includes multiple StatsItem entries.
class StatsResult(BaseModel):
    """Statistics result model"""
    query_time_in_millis: int = Field(..., description="Query time in milliseconds")
    result_time_in_millis: int = Field(..., description="Result time in milliseconds")
    stats: Dict[str, List[StatsItem]] = Field(
        default_factory=dict,
        description="Statistics by category"
    )
class Config:
  extra = 'allow'
  # Represents a single filter option in the search API.
  # Includes a concept ID, display label, and optionally the number
  # of matching ads for this filter. 
class FilterOption(BaseModel):
    """Filter option"""
    concept_id: Optional[str] = Field(None, description="Concept ID")
    label: str = Field(..., description="Display label")
    occurrences: Optional[int] = Field(None, description="Number of matching ads")
  # Represents the available filter options for a job search.
  # Each attribute contains a list of FilterOption objects for the respective category,
  # such as occupations, regions, municipalities, employment types, or occupation fields.
class FiltersResult(BaseModel):
    """Available filters result"""
    occupations: List[FilterOption] = Field(default_factory=list)
    regions: List[FilterOption] = Field(default_factory=list)
    municipalities: List[FilterOption] = Field(default_factory=list)
    employment_types: List[FilterOption] = Field(default_factory=list)
    occupation_fields: List[FilterOption] = Field(default_factory=list)