from fastapi import APIRouter, HTTPException
import time
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from StateGraph import graph
from langchain_core.messages import HumanMessage
from ..models import ChatResponse, ResponseStatus
from ..models import ChatRequest
from ..helpers import detect_expert_used, detect_language, detect_emergency

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for interacting with the AI assistant"""
    start_time = time.time()
    
    try:
        # Configure session
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Create input message
        input_message = {"messages": [HumanMessage(content=request.message)]}
        
        # Invoke the graph
        result = graph.invoke(input_message, config)
        
        # Process response
        if result and "messages" in result:
            ai_response = result["messages"][-1].content
            
            # Detect expert used and other metadata
            expert_used = detect_expert_used(ai_response)
            language_detected = detect_language(request.message)
            is_emergency = detect_emergency(request.message)
            
            response_time = int((time.time() - start_time) * 1000)
            
            return ChatResponse(
                status=ResponseStatus.SUCCESS,
                message=ai_response,
                session_id=request.session_id,
                timestamp=datetime.now(),
                expert_used=expert_used,
                language_detected=language_detected,
                is_emergency=is_emergency,
                response_time_ms=response_time
            )
        else:
            raise HTTPException(status_code=500, detail="No response generated")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")