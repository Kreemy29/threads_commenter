"""
FastAPI application entrypoint.
"""

import uvicorn
from fastapi import FastAPI
from app.api import router

# Create FastAPI app
app = FastAPI(
    title="Ava Comment Engine", 
    version="1.0.0",
    description="Thread comment generation service with DeepSeek"
)

# Include API router
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 