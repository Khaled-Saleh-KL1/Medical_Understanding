from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    session_id: Optional[str] = Field(default="default", description="Session identifier")
    language: Optional[str] = Field(default="auto", description="Preferred language (auto, en, ar)")
    
class SessionRequest(BaseModel):
    session_id: str = Field(..., description="Session to manage")

class HealthCheckRequest(BaseModel):
    service: Optional[str] = Field(default="all", description="Service to check")