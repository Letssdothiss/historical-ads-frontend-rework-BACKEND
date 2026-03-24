"""Export routes"""
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.models.schemas import ExportFormat
from app.services import get_api, get_processor, HistoricalAdsAPI, DataProcessor
from app.utils.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Export"])


@router.get("/export")
async def export(
    q: Optional[str] = Query(None),
    format: ExportFormat = Query(ExportFormat.JSON),
    limit: int = Query(1000, le=10000),
    published_before: Optional[str] = Query(None),
    published_after: Optional[str] = Query(None),
    occupation: Optional[List[str]] = Query(None),
    municipality: Optional[List[str]] = Query(None),
    region: Optional[List[str]] = Query(None),
    api: HistoricalAdsAPI = Depends(get_api),
    processor: DataProcessor = Depends(get_processor),
) -> Response:
    """Export job ads"""
    limit = min(limit, settings.MAX_EXPORT_RECORDS)
    
    result = await api.search(
        q=q, limit=limit,
        published_before=published_before,
        published_after=published_after,
        occupation=occupation,
        municipality=municipality,
        region=region,
    )
    
    ads = result.get("hits", [])
    filename = processor.filename(q, format.value)
    
    if format == ExportFormat.json:
        data = processor.to_json(ads).encode()
        media_type = "application/json"
        ext = ".json"
    elif format == ExportFormat.csv:
        data = processor.to_csv(ads).encode()
        media_type = "text/csv"
        ext = ".csv"
    else:
        data = processor.to_xlsx(ads)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ext = ".xlsx"
    
    return Response(
        content=data,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}{ext}"'},
    )