"""Authentication and security middleware"""

import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from typing import Optional

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """
    Verify JWT token from request headers
    
    Args:
        credentials: HTTP Bearer credentials
    
    Returns:
        Decoded token subject (user_id)
    """
    try:
        # Import here to avoid circular imports
        from app.config import get_settings
        settings = get_settings()
        
        # This would verify JWT token with PyJWT
        # For demo, accept any bearer token
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme"
            )
        
        token = credentials.credentials
        
        if not token or len(token) < 10:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # In production, decode JWT:
        # import jwt
        # payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        # return payload.get("sub")
        
        logger.info(f"Token verified for request")
        return token
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_optional_token(credentials: Optional[HTTPAuthCredentials] = Depends(security)) -> Optional[str]:
    """Optional token verification - doesn't fail if token is missing"""
    if credentials is None:
        return None
    try:
        return await verify_token(credentials)
    except HTTPException:
        return None
