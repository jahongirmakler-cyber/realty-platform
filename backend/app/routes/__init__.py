from .auth import router as auth_router
from .properties import router as properties_router
from .search import router as search_router
from .listings import router as listings_router
from .agents import router as agents_router
from .admin import router as admin_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "properties_router",
    "search_router",
    "listings_router",
    "agents_router",
    "admin_router",
    "users_router"
]