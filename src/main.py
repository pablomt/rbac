from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.utils.db import init_db, close_db
from src.routes.auth_routes import setup_routes
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB connection on startup
    await init_db()
    yield
    # Close DB connection on shutdown
    await close_db()

app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization Service",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
    allow_credentials=True,
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Setup routes
setup_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4,
        log_level="info",
        debug=True
    )

