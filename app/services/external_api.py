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
    # Search for job ads using the API with various filter parameters and pagination options.
    async def search(
        self,
        query: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
        published_before: Optional[str] = None,
        published_after: Optional[str] = None,
        occupation: Optional[List[str]] = None,
        occupation_group: Optional[List[str]] = None,
        occupation_field: Optional[List[str]] = None,
        municipality: Optional[List[str]] = None,
        region: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        employment_type: Optional[List[str]] = None,
        experience_required: Optional[bool] = None,
        ) -> Dict[str, Any]:
        """ Search for job ads using the API """
        params = {"offset": offset, "limit": limit}
        if query:
            params["q"] = query
        if published_before:
            params["published_before"] = published_before
        if published_after:
            params["published_after"] = published_after
        if occupation:
            params["occupation"] = occupation
        if occupation_group:
            params["occupation_group"] = occupation_group
        if occupation_field:
            params["occupation_field"] = occupation_field
        if municipality:
            params["municipality"] = municipality
        if region:
            params["region"] = region
        if country:
            params["country"] = country
        if employment_type:
            params["employment_type"] = employment_type
        if experience_required is not None:
            params["experience_required"] = experience_required
        url = self._build_url("search")
        
        try:
          async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
          return self._handle_response(response)
        except httpx.TimeoutException:
            raise TimeoutError(f"Request to {url} timed out")
        except httpx.ConnectError as e:
            raise ExternalAPIError(f"Failed to connect to {url}: {str(e)}")
      # Retrieve a specific job ad by its unique ID from the API.
    async def get_ad(self, ad_id: str) -> Dict[str, Any]:
        """Get a specific job ad by ID"""
        url = self._build_url(f"ad/{ad_id}")
      
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                return self._handle_response(response)
        except httpx.TimeoutException:
            raise TimeoutError("API request timed out")
        except httpx.ConnectError:
            raise ExternalAPIError("Failed to connect to API")
      # Retrieve statistics about job ads.
    async def get_stats(
        self,
        query: Optional[str] = None,
        published_before: Optional[str] = None,
        published_after: Optional[str] = None,
        occupation: Optional[List[str]] = None,
        occupation_group: Optional[List[str]] = None,
        occupation_field: Optional[List[str]] = None,
        municipality: Optional[List[str]] = None,
        region: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
         """Get statistics about job ads"""
         params = {}

         if query:
            params["q"] = query
         if published_before:
            params["published-before"] = published_before
         if published_after:
            params["published-after"] = published_after
         if occupation:
            params["occupation"] = occupation
         if occupation_group:
            params["occupation-group"] = occupation_group
         if occupation_field:
            params["occupation-field"] = occupation_field
         if municipality:
            params["municipality"] = municipality
         if region:
            params["region"] = region

         url = self._build_url("stats")
         try:
              async with httpx.AsyncClient(timeout=self.timeout) as client:
                  response = await client.get(url, params=params)
                  return self._handle_response(response)
         except httpx.TimeoutException:
              raise TimeoutError("API request timed out")
         except httpx.ConnectError:
              raise ExternalAPIError("Failed to connect to API")
# Singleton instance of the ExternalAPIClient to be used throughout the application.
_api_client: Optional[ExternalAPIClient] = None

def get_api_client() -> ExternalAPIClient:
    """ Get or create API client Instance """
    global _api_client
    if _api_client is None:
        _api_client = ExternalAPIClient()
    return _api_client