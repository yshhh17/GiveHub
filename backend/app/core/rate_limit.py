from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,  # Rate limit by IP address
    default_limits=["200/hour"],   # Default:  200 requests per hour per IP
    storage_uri="memory://",       # Use in-memory storage (or Redis for production)
    # For Redis: storage_uri="redis://localhost:6379"
)

# Custom rate limit exceeded handler
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors
    """
    logger.warning(f"Rate limit exceeded for IP: {get_remote_address(request)}")
    
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "detail": str(exc.detail)
        }
    )


# Custom key function to rate limit by user ID (for authenticated endpoints)
def get_user_identifier(request: Request) -> str:
    """
    Get user identifier for rate limiting
    Returns user email if authenticated, otherwise IP address
    """
    try:
        # Try to get user from request state (set by authentication)
        if hasattr(request.state, "user"):
            user = request.state.user
            return f"user:{user.email}"
        
        # Fallback to IP address
        return f"ip:{get_remote_address(request)}"
    except:
        return f"ip:{get_remote_address(request)}"


# User-based limiter
user_limiter = Limiter(
    key_func=get_user_identifier,
    default_limits=["100/hour"],
    storage_uri="memory://"
)