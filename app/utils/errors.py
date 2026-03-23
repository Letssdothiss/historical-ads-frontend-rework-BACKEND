"""
Custom error classes for the application.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

# 500 Internal Server Error
class APIError(HTTPException):
    """Base application error"""
    def __init__(
        self, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail: str = "An unexpected error occurred.",
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code or self.__class__.__name__
        super().__init__(status_code=status_code, detail=detail, headers=headers)
# 400 Bad Request
class BadRequestError(APIError):
  def __init__(self, detail: str = "Bad request."): 
    super().__init__(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=detail,
      error_code="BadRequestError"
    )
    