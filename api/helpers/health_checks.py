"""
Health check helper functions for the Medical Understanding AI API
"""
import sys
import os


def check_database_connection() -> str:
    """Check if database is accessible"""
    try:
        # Add src to path and check database
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
        from models.connect_database import memory_saver
        return "operational"
    except Exception as e:
        return f"error: {str(e)}"


def check_ai_model() -> str:
    """Check if AI model is loaded and responsive"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
        from nodes.LLM import base_model
        if base_model:
            return "operational"
        else:
            return "not_loaded"
    except Exception as e:
        return f"error: {str(e)}"


def check_tools_availability() -> str:
    """Check if all tools are available"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
        from tools import (
            WebSearchTool, 
            HumanAssistanceTool, 
            ConsultArabicDoctorTool, 
            ConsultArabicAIResearcherTool
        )
        return "operational"
    except Exception as e:
        return f"error: {str(e)}"
