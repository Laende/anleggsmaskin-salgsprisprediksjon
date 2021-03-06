import secrets
from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.core.config import get_settings

api_key_header = APIKeyHeader(name="token", auto_error=False)


def authenticate(header: Optional[str] = Security(api_key_header)) -> bool:
    settings = get_settings()
    if header is None:
        detail = "API key is missing."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers={})
    if not secrets.compare_digest(header, str(settings.API_KEY)):
        detail = "Invalid key. You are not authorized."
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={})
    return True
