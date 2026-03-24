"""
Search API routes
"""
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_api
from app.models import SearchResult, JobAd
from app.services.external_api import ExternalAPIClient
from app.utils.config import settings
from app.utils.errors import BadRequestError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=SearchResult)
async def search(
    q: Optional[str] = Query(None, description="Free text search query"),
    offset: int = Query(0, ge=0, description="Result offset"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    published_before: Optional[str] = Query(None, description="Published before date (YYYY-MM-DD)"),
    published_after: Optional[str] = Query(None, description="Published after date (YYYY-MM-DD)"),
    occupation: Optional[List[str]] = Query(None, description="Occupation IDs"),
    occupation_group: Optional[List[str]] = Query(None, description="Occupation group IDs"),
    occupation_field: Optional[List[str]] = Query(None, description="Occupation field IDs"),
    municipality: Optional[List[str]] = Query(None, description="Municipality"),
    region: Optional[List[str]] = Query(None, description="Region"),
    country: Optional[List[str]] = Query(None, description="Country"),
    employment_type: Optional[List[str]] = Query(None, description="Employment type"),
    experience_required: Optional[bool] = Query(None, description="Experience required"),
    api: ExternalAPIClient = Depends(get_api),
):
    """
    Search for historical job ads
    Search through historical job advertisements with various filters.
    """
    try:
        limit = min(limit, settings.MAX_PAGE_SIZE)
        
        result = await api.search(
            query=q,
            offset=offset,
            limit=limit,
            published_before=published_before,
            published_after=published_after,
            occupation=occupation,
            occupation_group=occupation_group,
            occupation_field=occupation_field,
            municipality=municipality,
            region=region,
            country=country,
            employment_type=employment_type,
            experience_required=experience_required,
        )
        
        return result
    
    except Exception as e:
        logger.exception(f"Search error: {e}")
        raise
      

@router.get("/ad/{ad_id}", response_model=JobAd, tags=["Ads"])
async def get_ad(
    ad_id: str,
    api: ExternalAPIClient = Depends(get_api),
):
    """
    Get a specific job ad by ID
    
    Retrieve a specific job advertisement by its unique identifier.
    """
    result = await api.get_ad(ad_id)
    return result