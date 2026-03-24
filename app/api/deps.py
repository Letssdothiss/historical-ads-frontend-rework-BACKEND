"""
API dependencies for dependency injection in FastAPI routes. This module defines functions that provide instances of the ExternalAPIClient, which can be injected into route handlers to interact with the external job ads API. The dependencies are designed to be easily testable and allow for mocking the API client during unit tests.
"""
from app.services.external_api import ExternalAPIClient, get_api_client
from app.services.data_processor import DataProcessor, get_data_processor
from app.utils.config import settings

def get_settings():
    """Get application settings"""
    return settings
def get_api() -> ExternalAPIClient:
    """Get API client instance for dependency injection"""
    return get_api_client()
def get_processor() -> DataProcessor:
    """Get data processor instance for dependency injection"""
    return get_data_processor()
  
