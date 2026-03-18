from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.v1.endpoints import (
  search
)

# Create FastAPI instance
app = FastAPI(
  root_path='/',
  title='API Title',
  description='API managing historical ads',
  version='0.0.1'
)

# Exception handler template
#
@app.exception_handler(ValueError)
async def type_of_error_handler(
  request: Request,
  exc: ValueError
) -> JSONResponse:
  return JSONResponse(
    status_code=400,
    content={"detail": str(exc)}
  )

# Enable CORS to enable access from client to API
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    'http://localhost:5173',
    'http://0.0.0.0:8083',
    'client origin'
  ], # Adjust for frontend
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

# Include routers
app.include_router(search.router)

# Health check
@app.get('/')
def read_root():
  """API health check"""
  return {"message": "It's your lucky day. The API is up and running!"}
