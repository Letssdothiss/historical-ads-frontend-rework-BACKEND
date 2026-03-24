from fastapi import APIRouter, HTTPException
from app.services.ad_service import fetch_historical_ad

router = APIRouter(
    prefix="/api/v1/ad",
    tags=["ad"],
)

@router.get("/{id}")
async def ad_endpoint(id: str):
    """
    Fetch historical ad based on ID.
    """
    result = await fetch_historical_ad(id)
    if not result:
        raise HTTPException(status_code=404, detail="No ad found.")
    return result
