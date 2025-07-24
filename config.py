"""Configuration settings for the TROOPERS Chatbot"""

import os
from typing import Dict, Any

# Webhook Configuration
WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://primary-production-6654.up.railway.app/webhook/f1deda52-3942-419c-879b-5b8b0f28743e",
)

# App Configuration
APP_CONFIG: Dict[str, Any] = {
    "page_title": "TROOPERS Assistant",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

# Chat Configuration
CHAT_CONFIG: Dict[str, Any] = {
    "welcome_message": """Welcome to TROOPERS! So glad you're here! 😊

To get started and recommend the best team mix for your project, could you please tell me what kind of project or event you are planning? For example, is it a Café/Restaurant Service, Retail Promotion, Roadshow, Warehouse Operations, or something else? This helps me tailor the roles to your needs.""",
    "input_placeholder": "Ask about part-time jobs, hiring, or anything else...",
    "timeout_seconds": 30,
    "retry_attempts": 3,
}

# Styling Configuration
CUSTOM_CSS = """
<style>
    .main {
        padding: 0rem 1rem;
    }
    
    .chat-header {
        background: linear-gradient(90deg, #007ACC 0%, #0056A3 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .session-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #007ACC;
    }
    
    .stChatMessage {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
"""
