from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import init_db, close_db
from app.routes import (
    auth_router,
    properties_router,
    search_router,
    listings_router,
    agents_router,
    admin_router,
    users_router
)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title="Realty Platform API",
    description="Professional Real Estate Marketplace for Uzbekistan",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(properties_router)
app.include_router(search_router)
app.include_router(listings_router)
app.include_router(agents_router)
app.include_router(admin_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {
        "message": "Uzbekistan Real Estate Marketplace API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )