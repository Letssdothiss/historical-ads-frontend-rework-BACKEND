"""Search routes"""
import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query

from app.services import get_api, HistoricalAdsAPI

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Search"])


@router.get("/search")
async def search(
    q: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_before: Optional[str] = Query(None),
    published_after: Optional[str] = Query(None),
    occupation: Optional[List[str]] = Query(None),
    occupation_group: Optional[List[str]] = Query(None),
    occupation_field: Optional[List[str]] = Query(None),
    municipality: Optional[List[str]] = Query(None),
    region: Optional[List[str]] = Query(None),
    country: Optional[List[str]] = Query(None),
    employment_type: Optional[List[str]] = Query(None),
    experience_required: Optional[bool] = Query(None),
    api: HistoricalAdsAPI = Depends(get_api),
) -> Dict[str, Any]:
    """Search historical job ads"""
    return await api.search(
        q=q, offset=offset, limit=limit,
        published_before=published_before, published_after=published_after,
        occupation=occupation, occupation_group=occupation_group,
        occupation_field=occupation_field, municipality=municipality,
        region=region, country=country, employment_type=employment_type,
        experience_required=experience_required,
    )


@router.get("/search/ad/{ad_id}")
async def get_ad(ad_id: str, api: HistoricalAdsAPI = Depends(get_api)) -> Dict[str, Any]:
    """Get specific job ad"""
    return await api.get_ad(ad_id)