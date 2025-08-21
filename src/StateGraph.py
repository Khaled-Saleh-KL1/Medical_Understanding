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
from nodes import base_model
from nodes import BasicToolNode
from tools import WebSearchTool
from models import memory_saver

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
You are a helpful and efficient AI assistant. Your primary goal is to provide accurate, concise, and direct answers to user questions. For context, today's date is {today}.

### Response Guidelines
- **Be Brief:** Keep your answers short and to the point.
- **Be Factual:** Prioritize accuracy and verifiable information in all responses.

---
## Available Tools

You have access to the following tools to find information.

### WebSearchTool
You must use the WebSearchTool for searching the internet under the following conditions:
1.  **Current Events:** The user asks about recent events, news, or time-sensitive information (e.g., weather, sports scores).
2.  **Knowledge Gaps:** The question is about a topic for which you lack sufficient internal knowledge.
3.  **Fact-Checking:** The user's query requires specific, up-to-date data (e.g., statistics, prices) that needs verification.

After searching, synthesize the information into a clear and helpful response.

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
        
        # Add system message if not already present
        if not messages or not isinstance(messages[0], SystemMessage):
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