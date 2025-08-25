from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from enum import Enum

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

class ExpertType(str, Enum):
    DOCTOR = "doctor"
    AI_RESEARCHER = "ai_researcher"
    WEB_SEARCH = "WebSearch"
    HUMAN = "human"
    NONE = "none"

class ChatResponse(BaseModel):
    status: ResponseStatus
    message: str
    session_id: str
    timestamp: datetime
    expert_used: Optional[ExpertType] = None
    language_detected: Optional[str] = None
    is_emergency: Optional[bool] = False
    response_time_ms: Optional[int] = None

class HealthCheckResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime
    services: Dict[str, str]
    version: str

class ErrorResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ERROR
    error: str
    detail: Optional[str] = None
    timestamp: datetime