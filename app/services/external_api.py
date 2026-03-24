"""
External APi client for Historical Ads API
"""
import logging 
from typing import Any, Dict, List, Optional
import httpx

from app.utils.config import settings
from app.utils.errors import ExternalAPIError, NotFoundError, ConflictError, TimeoutError
logger = logging.getLogger(__name__)
# The ExternalAPIClient class provides methods to interact with the Historical Ads API,
# including searching for job ads, retrieving statistics, and exporting data.
class ExternalAPIClient:
  """ Client for the Historical Ads API """
  def __init__(
    self,
    base_url: Optional[str] = None,
    timeout: Optional[int] = None,
    ):
    self.base_url = base_url or settings.EXTERNAL_API_BASE_URL
    self.timeout = timeout or settings.EXTERNAL_API_TIMEOUT