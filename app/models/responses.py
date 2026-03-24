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
    