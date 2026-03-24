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
