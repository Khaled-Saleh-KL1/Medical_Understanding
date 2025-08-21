#!/bin/bash

# LangGraph Chatbot Setup Script

echo "🚀 Setting up LangGraph Chatbot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "🔧 Setting up environment file..."
    cp .example.env .env
    echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
else
    echo "✅ Environment file already exists"
fi

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Run: python Run_Chatbot.py"
echo ""
echo "Get your API key from: https://makersuite.google.com/app/apikey"
