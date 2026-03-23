from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ad_service import fetch_historical_ad

class AdRequest(BaseModel):
    id: str

router = APIRouter(
    prefix="/api/v1/ad",
    tags=["ad"],
)

@router.post("/")
async def ad_endpoint(request: AdRequest):
    """
    Fetch historical ad based on ID.
    """
    result = await fetch_historical_ad(request.id)
    if not result:
        raise HTTPException(status_code=404, detail="No ad found.")
    return result
