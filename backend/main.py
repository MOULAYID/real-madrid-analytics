"""
FastAPI Server Entry Point for Real Madrid Financial Intelligence Dashboard
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.analytics import router as analytics_router

app = FastAPI(
    title="Real Madrid Financial Intelligence API",
    description="Analytics REST API supporting the 7-page executive financial dashboard",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Real Madrid Financial Intelligence API",
        "version": "1.0.0",
        "documentation": "/docs"
    }
