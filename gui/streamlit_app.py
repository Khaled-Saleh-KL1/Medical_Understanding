"""
Streamlit GUI for Medical Understanding Chatbot
A web-based interface for interacting with the medical AI assistant
"""

import streamlit as st
import requests
import uuid
import json
from datetime import datetime
import sys
import os

# Add src to path for direct access
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Try to import directly if API is not running
try:
    from StateGraph import graph
    from langchain_core.messages import HumanMessage
    DIRECT_MODE = True
except ImportError:
    DIRECT_MODE = False

# Page configuration
st.set_page_config(
    page_title="Medical/AI/General Assistant",
    page_icon="🏥🤖🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stChatMessage {
        background-color: #2d3032;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #2d3032;
        text-align: right;
    }
    .assistant-message {
        background-color: #2d3032;
    }
    .emergency-alert {
        background-color: #2d3032;
        border: 2px solid #f44336;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_mode" not in st.session_state:
        st.session_state.api_mode = False

def call_chatbot_direct(message: str) -> dict:
    """Call the chatbot directly using StateGraph"""
    try:
        config = {"configurable": {"thread_id": st.session_state.session_id}}
        input_message = {"messages": [HumanMessage(content=message)]}
        
        result = graph.invoke(input_message, config)
        
        if result and "messages" in result:
            ai_response = result["messages"][-1].content
            return {
                "status": "success",
                "message": ai_response,
                "session_id": st.session_state.session_id,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {"status": "error", "message": "No response generated"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

def call_chatbot_api(message: str, api_url: str = "http://localhost:8000") -> dict:
    """Call the chatbot via FastAPI"""
    try:
        response = requests.post(
            f"{api_url}/chat/",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"API Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Connection Error: {str(e)}"}

def display_message(role: str, content: str, timestamp: str = None):
    """Display a message in the chat interface"""
    with st.chat_message(role):
        st.write(content)
        if timestamp:
            st.caption(f"🕒 {timestamp}")

def main():
    """Main Streamlit application"""
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🏥 Medical AI Assistant")
        st.markdown("---")
        
        # Session info
        st.subheader("Session Info")
        st.text(f"ID: {st.session_state.session_id[:8]}...")
        
        # Mode selection
        st.subheader("Connection Mode")
        api_mode = st.checkbox("Use API Mode", value=st.session_state.api_mode)
        st.session_state.api_mode = api_mode
        
        if api_mode:
            api_url = st.text_input("API URL", value="http://localhost:8000")
            # Test API connection
            if st.button("Test API Connection"):
                try:
                    response = requests.get(f"{api_url}/health", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ API Connected")
                    else:
                        st.error("❌ API Connection Failed")
                except:
                    st.error("❌ Cannot reach API")
        else:
            if DIRECT_MODE:
                st.success("✅ Direct Mode Available")
            else:
                st.error("❌ Direct Mode Unavailable")
        
        st.markdown("---")
        
        # New conversation
        if st.button("🔄 New Conversation"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Features info
        st.subheader("🎯 Features")
        st.markdown("""
        - 🩺 Medical expertise
        - 🔬 AI research assistance
        - 🌍 Multilingual (EN/AR)
        - 🚨 Emergency detection
        - 💾 Conversation memory
        - 🔍 Web search capability
        """)
        
        # Emergency notice
        st.markdown("---")
        st.error("🚨 **Emergency?** Call local emergency services immediately!")

    # Main chat interface
    st.title("💬 Chat with Medical AI")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            display_message(
                message["role"], 
                message["content"], 
                message.get("timestamp")
            )
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about health and medicine..."):
        # Add user message
        user_timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": user_timestamp
        })
        
        # Display user message
        display_message("user", prompt, user_timestamp)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if st.session_state.api_mode:
                    response = call_chatbot_api(prompt, api_url)
                else:
                    response = call_chatbot_direct(prompt)
                
                if response["status"] == "success":
                    ai_message = response["message"]
                    ai_timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    # Check for emergency keywords
                    emergency_keywords = ["emergency", "urgent", "critical", "severe", "911", "emergency room"]
                    if any(keyword in prompt.lower() for keyword in emergency_keywords):
                        st.markdown("""
                        <div class="emergency-alert">
                        🚨 <strong>EMERGENCY DETECTED</strong><br>
                        If this is a medical emergency, please contact your local emergency services immediately!
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write(ai_message)
                    st.caption(f"🕒 {ai_timestamp}")
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_message,
                        "timestamp": ai_timestamp
                    })
                else:
                    error_message = response["message"]
                    st.error(f"❌ {error_message}")
                    
                    # Add error message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {error_message}",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

if __name__ == "__main__":
    main()
