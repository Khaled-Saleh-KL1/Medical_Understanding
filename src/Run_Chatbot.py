"""
LangGraph Chatbot Runner
A simple interactive chatbot using LangGraph and Google's Gemini model.
"""

import uuid
from StateGraph import graph

# Generate a unique thread_id for this session
THREAD_ID = str(uuid.uuid4())

def stream_graph_updates(user_input: str):
    """Stream updates from the graph for a given user input."""
    try:
        final_response = None
        # Include the config with thread_id for PostgreSQL checkpointer
        config = {"configurable": {"thread_id": THREAD_ID}}
        
        # Create a HumanMessage for the user input
        from langchain_core.messages import HumanMessage
        
        # Add more detailed error handling
        for event in graph.stream({"messages": [HumanMessage(content=user_input)]}, config=config):
            for node_name, value in event.items():
                if "messages" in value and value["messages"]:
                    last_message = value["messages"][-1]
                    # Only show the final assistant response (from chatbot node)
                    if node_name == "chatbot" and hasattr(last_message, 'content'):
                        final_response = last_message.content
        
        # Print only the final response without "Assistant:" prefix
        if final_response:
            print(final_response)
    except Exception as e:
        print(f"Error processing your request: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()

def main():
    """Main chatbot loop."""
    global THREAD_ID

    print("🤖 LangGraph Chatbot")
    print(f"Session ID: {THREAD_ID}")
    print("This conversation will be stored in PostgreSQL for memory persistence.")
    print("Type 'quit', 'exit', or 'q' to end the conversation.")
    print("Type 'new' to start a new conversation thread.\n")
    
    while True:
        try:
            print("================================ Human Message =================================")
            user_input = input("User: ")
            if user_input.lower().strip() in ["quit", "exit", "q"]:
                print("Goodbye! 👋")
                break
            elif user_input.lower().strip() == "new":
                THREAD_ID = str(uuid.uuid4())
                print(f"Started new conversation thread: {THREAD_ID}")
                continue
            
            if user_input.strip():  # Only process non-empty input
                print("================================== Ai Message ==================================")
                stream_graph_updates(user_input)
            else:
                print("Please enter a message.")
                
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except EOFError:
            # Fallback if input() is not available (e.g., in some environments)
            user_input = "I wanted to ask you about.."
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()