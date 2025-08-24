from langchain_google_genai import ChatGoogleGenerativeAI
import os
from tools import (
    WebSearchTool, 
    HumanAssistanceTool, 
    ConsultDoctorTool, 
    ConsultAIResearcherTool,
    MultilingualSupportTool,
    ConsultArabicDoctorTool,
    ConsultArabicAIResearcherTool
)

# Create the base LLM model
try:
    base_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    ).bind_tools([
        WebSearchTool, 
        HumanAssistanceTool, 
        ConsultDoctorTool, 
        ConsultAIResearcherTool,
        MultilingualSupportTool,
        ConsultArabicDoctorTool,
        ConsultArabicAIResearcherTool
    ])
except:
    print("GEMINI_API_KEY is not provided")