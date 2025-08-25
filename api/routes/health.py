from fastapi import APIRouter
from datetime import datetime
from ..models import HealthCheckResponse
from ..helpers import check_database_connection, check_ai_model, check_tools_availability

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthCheckResponse)
async def health_check():
    """System health check endpoint"""
    try:
        # Check various services
        services = {
            "database": check_database_connection(),
            "ai_model": check_ai_model(),
            "tools": check_tools_availability(),
        }
        
        return HealthCheckResponse(
            status="healthy",
            message="All systems operational",
            timestamp=datetime.now(),
            services=services,
            version="1.0.0"
        )
    except Exception as e:
        return HealthCheckResponse(
            status="unhealthy",
            message=f"System issues detected: {str(e)}",
            timestamp=datetime.now(),
            services={},
            version="1.0.0"
        )