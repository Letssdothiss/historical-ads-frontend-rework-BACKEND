from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.search_service import search_historical_ads, SearchResult

class SearchRequest(BaseModel):
    query: str

router = APIRouter(
    prefix="/api/v1/search",
    tags=["search"],
)

@router.post("/", response_model=List[SearchResult])
async def search_endpoint(request: SearchRequest):
    """
    Search for historical ads based on a search query.
    """
    results = search_historical_ads(request.query)
    if not results:
        raise HTTPException(status_code=404, detail="No results found.")
    return results
