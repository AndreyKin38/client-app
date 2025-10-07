from backend.handlers.app import router as app_router
from backend.handlers.user import router as user_router
from backend.handlers.auth import router as auth_router


__all__ = [
    'app_router',
    'user_router',
    'auth_router'
]

