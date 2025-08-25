# Load Environment Variables
from dotenv import load_dotenv
load_dotenv()

# Load Libraries
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, AIMessage
import datetime

# Load from Files
from nodes import base_model, BasicToolNode
from models import memory_saver
from tools import (
    WebSearchTool, 
    HumanAssistanceTool, 
    ConsultDoctorTool, 
    ConsultAIResearcherTool,
    MultilingualSupportTool,
    ConsultArabicDoctorTool,
    ConsultArabicAIResearcherTool,
    ConsultGeneralExpertTool
)

# For developers - log files
# =======================================================
import os
import logging
log_directory = "log"
os.makedirs(log_directory, exist_ok=True)
log_file_path = os.path.join(log_directory, "errors.log")
# Configure the logging system
logging.basicConfig(
    filename=log_file_path,  # The file to log to
    level=logging.ERROR,     # Only log ERROR and CRITICAL messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # The format of the log messages
    filemode='a' # Append to the file
)
logger = logging.getLogger(__name__)
# =======================================================

# State class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# System message configuration
today = datetime.datetime.now().date().strftime("%d-%b-%Y")
system_message = f"""
You are a helpful and efficient AI assistant with multilingual capabilities (Arabic and English). Your primary goal is to provide accurate, concise, and direct answers to user questions in their preferred language. For context, today's date is {today}.

### Response Guidelines
- **Be Brief:** Keep your answers short and to the point.
- **Be Factual:** Prioritize accuracy and verifiable information in all responses.
- **Language Detection:** Automatically detect if the user is communicating in Arabic or English and respond accordingly.
- **Cultural Sensitivity:** Be respectful of cultural contexts when responding in Arabic.

---
## IMPORTANT: Tool Usage Protocol

**STEP 1: ALWAYS use MultilingualSupportTool FIRST** for every user input to:
- Detect the user's language (Arabic or English)
- Get proper response guidance for that language
- Ensure consistent language throughout the conversation

**STEP 2: Choose the appropriate expert tool based on the question type:**

### Medical & Health Questions → ConsultArabicDoctorTool
Use this tool for ALL medical and health-related questions in ANY language:
- Medical symptoms or health concerns
- Questions about medications, treatments, or medical procedures
- Health advice or medical education questions
- Anatomy, physiology, or medical condition inquiries
- Emergency medical situations

### AI & Technology Questions → ConsultArabicAIResearcherTool  
Use this tool for ALL AI and technology-related questions in ANY language:
- Artificial intelligence, machine learning, or deep learning questions
- Technical implementation help with AI frameworks or models
- Questions about recent AI developments or research papers
- Programming and AI development best practices
- Technical AI terminology and concepts

### General Knowledge Questions → ConsultGeneralExpertTool
Use this tool for ALL other educational and informational questions in ANY language:
- History, science, literature, culture, geography
- Educational topics and learning questions
- General "what is", "how does", "explain" questions
- Arts, philosophy, humanities, and social sciences
- General facts, trivia, and explanations of phenomena
- Non-medical, non-AI academic or intellectual inquiries

### Current Events & Web Information → WebSearchTool
Use this tool when you need real-time or recent information:
- Current events, news, or time-sensitive information
- Recent statistics, prices, or data that needs verification
- Weather, sports scores, or other current information
- Fact-checking recent developments

### Complex Human Situations → HumanAssistanceTool
Use this as a last resort when:
- The question requires human judgment beyond expert tools
- Sensitive personal situations requiring empathy
- Tool failures or technical difficulties
- Complex ethical or moral dilemmas

---
## Available Tools

### MultilingualSupportTool
**ALWAYS USE THIS FIRST** - Detects user language and provides response guidance:
1. **Language Detection:** Automatically detects Arabic or English input
2. **Response Guidance:** Provides instructions for culturally appropriate responses
3. **Consistency:** Ensures all subsequent responses match the user's language

### ConsultArabicDoctorTool  
Provides medical expertise in user's preferred language:
- Handles medical terminology in both Arabic and English
- Provides culturally sensitive health advice
- Includes emergency escalation protocols
- Adapts medical explanations to cultural context

### ConsultArabicAIResearcherTool
Provides AI/technology expertise in user's preferred language:
- Handles technical terminology in both Arabic and English
- Explains AI concepts with cultural context
- Provides programming help and best practices
- Covers recent AI research and developments

### ConsultGeneralExpertTool
Provides general knowledge expertise in user's preferred language:
- Covers history, science, literature, culture, geography
- Educational and academic topics
- General explanations and learning support
- Arts, philosophy, and humanities

### WebSearchTool
Searches the internet for current information:
- Recent events, news, and time-sensitive data
- Up-to-date statistics and verification
- Current weather, sports, and live information

### HumanAssistanceTool
Connects with human assistance for complex situations:
- Sensitive personal matters requiring human empathy
- Complex ethical or judgment-based questions
- Situations beyond the scope of expert tools

After using any tool, synthesize the information into a clear and helpful response in the user's detected language.

---
## Tool Error Handling Protocol

If a required tool fails to execute for any reason (e.g., missing API key, network error), you must follow these rules:
1.  **Halt Execution:** Do not attempt to answer the question without the tool.
2.  **Identify the Failed Tool:** Determine the name of the tool that malfunctioned.
3.  **Inform the User:** Respond to the user with the exact format below, replacing `{{tool_name}}` with the name of the tool that failed.

**Required Response Format:**
"I am sorry, but I cannot complete your request because the `{{tool_name}}` tool is not configured correctly. Please provide the necessary API key or credentials to proceed."
"""

# Initialize the chatbot
def chatbot(state: State):
    """Main chatbot node that processes messages using the LLM."""
    try:
        messages = state["messages"]
        
        # Add system message ONLY if the message list is completely empty
        # This preserves conversation history while ensuring system message exists
        if not messages:
            system_msg = SystemMessage(content=system_message)
            messages = [system_msg]
        elif not isinstance(messages[0], SystemMessage):
            # If there are messages but no system message at the start, add it
            system_msg = SystemMessage(content=system_message)
            messages = [system_msg] + messages
        
        response = base_model.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        logger.exception("An error occurred during LLM model invocation")
        
        # Return a user-friendly error message as proper LangChain message
        error_response = AIMessage(content="I apologize, but I encountered an error.")
        return {"messages": [error_response]}

def route_tools(state: State):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

# Create tool node using tools from LLM model
tool_node = BasicToolNode(
    tools=[
        WebSearchTool,
        HumanAssistanceTool,
        ConsultDoctorTool,
        ConsultAIResearcherTool,
        MultilingualSupportTool,
        ConsultArabicDoctorTool,
        ConsultArabicAIResearcherTool,
        ConsultGeneralExpertTool
    ])

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to 
    # interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile(checkpointer=memory_saver)