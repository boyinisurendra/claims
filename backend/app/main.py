from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes
from .database import init_db
from .config import settings
import logging

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insurance Claim Review Assistant",
    description="AI-powered claim processing and validation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "claim-review-assistant"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Insurance Claim Review Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
