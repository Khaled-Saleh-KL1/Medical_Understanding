from langchain_tavily import TavilySearch

"""A tool that uses the Tavily Search API to find real-time information online.

This tool is used by an agent to answer questions about current events,
or any topic that requires up-to-date knowledge from the web. It is
configured to return a maximum of two search results for conciseness.
"""
try:
    WebSearchTool = TavilySearch(max_results=2)
except:
    print("TAVILY_API_KEY is not provided")