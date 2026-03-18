from pydantic import BaseModel

class SearchResult(BaseModel):
    search: str

def search_historical_ads(query: str) -> list[SearchResult]:
    # TODO: Implement search
    return [SearchResult(search=query)]
