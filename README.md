# LangGraph Chatbot

A simple yet powerful chatbot implementation using LangGraph and Google's Gemini AI model.

## Features

- 🤖 Interactive chat interface
- 🔄 Stream processing with LangGraph
- 🛡️ Error handling and graceful fallbacks
- 📊 Graph visualization capabilities
- 🔐 Environment-based API key management

## Project Structure

```
LangGraph_Doc/
├── Run_Chatbot.py          # Main chatbot runner
├── StateGraph.py           # LangGraph state and graph definition
├── nodes/                  # Node modules
│   ├── __init__.py        # Package initialization
│   ├── LLM.py             # LLM model configuration
│   └── visualize_graph.py # Graph visualization utilities
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── .example.env           # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up API Key

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy `.example.env` to `.env`:
   ```bash
   cp .example.env .env
   ```
3. Add your API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 3. Run the Chatbot

```bash
python Run_Chatbot.py
```

## Usage

Once running, you can:
- Type messages to chat with the AI
- Type `quit`, `exit`, or `q` to end the conversation
- Use Ctrl+C to force quit

## Graph Visualization

To visualize the graph structure, run:

```bash
python nodes/visualize_graph.py
```

For Jupyter environments, you can use the visualization functions directly.

## Dependencies

- `langgraph`: State graph framework
- `langchain-google-genai`: Google Gemini integration
- `python-dotenv`: Environment variable management
- `typing-extensions`: Enhanced type hints

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key

## Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Use the `.example.env` as a template for sharing

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
2. **API errors**: Check your API key and internet connection
3. **Visualization issues**: Install additional dependencies: `pip install pygraphviz pillow`

### Error Messages

The chatbot includes comprehensive error handling and will provide helpful error messages for common issues.

## Contributing

Feel free to extend this chatbot by:
- Adding new nodes to the graph
- Implementing different LLM providers
- Adding conversation memory
- Creating custom message processing logic

## License

This project is open source. Feel free to use and modify as needed.
