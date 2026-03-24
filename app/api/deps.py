"""API dependencies"""
from app.services.external_api import HistoricalAdsAPI, get_api
from app.services.data_processor import DataProcessor, get_processor
from app.utils.config import settings


def get_settings():
    """Get settings"""
    return settings