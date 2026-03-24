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
    
    # build full URLs for the API endpoints
    def _build_url(self, endpoint: str) -> str:
        """Build full URL for an endpoint """
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """ Handle API response and errors """
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise ExternalAPIError(f"Bad request: {response.text}")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.text}")
        elif response.status_code == 409:
            raise ConflictError(f"Duplicate ID: {response.text}")
        elif response.status_code == 500:
            raise ExternalAPIError(f"Server error: {response.url}")
        else:
            raise ExternalAPIError(f"Unexpected error (status {response.status_code})")
          