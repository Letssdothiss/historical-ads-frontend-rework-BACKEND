"""Statistics routes"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query

from app.services import get_api, HistoricalAdsAPI

router = APIRouter(tags=["Statistics"])


@router.get("/stats")
async def get_stats(
    q: Optional[str] = Query(None),
    published_before: Optional[str] = Query(None),
    published_after: Optional[str] = Query(None),
    occupation: Optional[List[str]] = Query(None),
    occupation_group: Optional[List[str]] = Query(None),
    occupation_field: Optional[List[str]] = Query(None),
    municipality: Optional[List[str]] = Query(None),
    region: Optional[List[str]] = Query(None),
    api: HistoricalAdsAPI = Depends(get_api),
) -> Dict[str, Any]:
    """Get statistics about job ads"""
    return await api.get_stats(
        q=q,
        published_before=published_before,
        published_after=published_after,
        occupation=occupation,
        occupation_group=occupation_group,
        occupation_field=occupation_field,
        municipality=municipality,
        region=region,
    )