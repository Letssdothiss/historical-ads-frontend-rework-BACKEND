"""
Service module
"""
from .external_api import ExternalAPIService, get_api_client
from .data_processor import DataProcessor, get_data_processor

__all__ = [
    'ExternalAPIService',
    'get_api_client',
    'DataProcessor',
    'get_data_processor'
]
