import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL")

async def fetch_historical_ad(id: str) -> dict:
    """
    Fetch historical ad from AF based on id.
    """
    url = f"{API_URL}/ad/{id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
