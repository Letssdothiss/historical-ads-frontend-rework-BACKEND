"""Filters routes"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, Query

from app.services import get_api, get_processor, HistoricalAdsAPI, DataProcessor

router = APIRouter(tags=["Filters"])


@router.get("/filters")
async def get_filters(
    q: Optional[str] = Query(None),
    api: HistoricalAdsAPI = Depends(get_api),
    processor: DataProcessor = Depends(get_processor),
) -> Dict[str, Any]:
    """Get available filter options"""
    stats = await api.get_stats(q=q)
    return processor.extract_filters(stats)


@router.get("/filters/occupations")
async def get_occupations(
    q: Optional[str] = Query(None),
    api: HistoricalAdsAPI = Depends(get_api),
):
    """Get occupation filter options"""
    stats = await api.get_stats(q=q)
    return {"occupations": stats.get("stats", {}).get("occupation-name", [])[:50]}


@router.get("/filters/regions")
async def get_regions(
    q: Optional[str] = Query(None),
    api: HistoricalAdsAPI = Depends(get_api),
):
    """Get region filter options"""
    stats = await api.get_stats(q=q)
    return {"regions": stats.get("stats", {}).get("region", [])}


@router.get("/filters/municipalities")
async def get_municipalities(
    q: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    api: HistoricalAdsAPI = Depends(get_api),
):
    """Get municipality filter options"""
    stats = await api.get_stats(q=q)
    return {"municipalities": stats.get("stats", {}).get("municipality", [])[:limit]}
