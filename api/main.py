from fastapi import FastAPI, HTTPException
from datetime import datetime

from .routes import chat, health
from .models import ErrorResponse, ResponseStatus

# Create FastAPI app
app = FastAPI(
    title="Medical Understanding AI API",
    description="AI-powered medical assistant with expert consultations and multilingual support",
    version="1.0.0"
)

# Include routers
app.include_router(chat.router)
app.include_router(health.router)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return ErrorResponse(
        error=exc.detail,
        detail=f"HTTP {exc.status_code}",
        timestamp=datetime.now()
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Medical Understanding AI API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health"
    }