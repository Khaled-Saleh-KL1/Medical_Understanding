"""
Graph Visualization Module
Saves LangGraph structure as PNG images to assets/visualize folder.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from StateGraph import graph

def save_graph_image():
    """Save the graph visualization to assets/visualize folder."""
    try:
        # Generate the graph image
        png_data = graph.get_graph().draw_mermaid_png()
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graph_{timestamp}.png"
        
        # Create the full path to assets/visualize
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_path = os.path.join(project_root, "assets", "visualize")
        full_path = os.path.join(assets_path, filename)
        
        # Create directories if they don't exist
        os.makedirs(assets_path, exist_ok=True)
        
        # Save the image
        with open(full_path, "wb") as f:
            f.write(png_data)
        
        print(f"✅ Graph saved: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Install dependencies: pip install pygraphviz pillow")
        return None

def print_graph_info():
    """Print basic graph information."""
    try:
        nodes = graph.get_graph().nodes
        edges = graph.get_graph().edges
        
        print("📊 Graph Structure:")
        print(f"   Nodes: {list(nodes.keys())}")
        print(f"   Edges: {[(edge.source, edge.target) for edge in edges]}")
        
    except Exception as e:
        print(f"❌ Error reading graph: {e}")

if __name__ == "__main__":
    print("🔍 LangGraph Visualizer")
    print_graph_info()
    save_graph_image()