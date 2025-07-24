#!/bin/bash

# TROOPERS Chatbot Launcher Script

echo "🤖 Starting TROOPERS Chatbot..."
echo "================================"

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Launching application..."
echo "🌐 Opening browser at http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
streamlit run app.py --server.address localhost --server.port 8501 