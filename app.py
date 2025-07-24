import streamlit as st
import requests
import json
import re
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
WEBHOOK_URL = "https://primary-production-6654.up.railway.app/webhook/f1deda52-3942-419c-879b-5b8b0f28743e"

# Page configuration
st.set_page_config(
    page_title="TROOPERS Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS with TROOPERS brand colors and minimal design
st.markdown(
    """
<style>
    /* Hide Streamlit default elements for cleaner look */
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .main {
        padding: 1rem 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Minimal header */
    .troopers-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .troopers-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1F2937;
        margin: 0;
    }
    
    .troopers-subtitle {
        font-size: 0.9rem;
        color: #6B7280;
        margin: 0.25rem 0 0 0;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        border: none;
    }
    
    /* User messages - TROOPERS brand blue */
    .stChatMessage[data-testid="user-message"] {
        background-color: #3B82F6;
        color: white;
    }
    
    /* Assistant messages - clean gray */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #F9FAFB;
        color: #374151;
        border: 1px solid #E5E7EB;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        border-radius: 24px;
        border: 2px solid #E5E7EB;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Minimal loading spinner */
    .minimal-spinner {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #6B7280;
        font-size: 0.9rem;
    }
    
    .spinner {
        width: 16px;
        height: 16px;
        border: 2px solid #E5E7EB;
        border-top: 2px solid #3B82F6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #FAFAFA;
    }
    
    /* Session info - minimal */
    .session-info {
        background-color: #F3F4F6;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.8rem;
        color: #6B7280;
        border-left: 3px solid #3B82F6;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-top: 0.25rem;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: #F9FAFB;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border: 1px solid #E5E7EB;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #F9FAFB;
        color: #374151;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #F3F4F6;
        border-color: #D1D5DB;
    }
    
    /* Hide default Streamlit padding */
    .block-container {
        padding: 1rem 0rem 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Welcome to TROOPERS! So glad you're here! 😊\n\nTo get started and recommend the best team mix for your project, could you please tell me what kind of project or event you are planning? For example, is it a Café/Restaurant Service, Retail Promotion, Roadshow, Warehouse Operations, or something else? This helps me tailor the roles to your needs.",
                "timestamp": datetime.now(),
            }
        ]

    if "session_id" not in st.session_state:
        st.session_state.session_id = (
            f"session_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        )

    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False


def send_message_to_webhook(message: str, session_id: str) -> Dict[str, Any]:
    """Send message to n8n webhook and return response"""
    try:
        payload = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "sessionId": session_id,
        }

        headers = {"Content-Type": "application/json"}

        logger.info(f"Sending message to webhook: {message}")

        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=30)

        response.raise_for_status()

        # Check content type to handle different response formats
        content_type = response.headers.get("content-type", "").lower()
        response_text = ""

        if "application/json" in content_type:
            # Handle JSON response (expected format)
            try:
                data = response.json()
                logger.info(f"JSON Webhook response: {data}")

                # Handle array response from n8n
                if isinstance(data, list) and len(data) > 0:
                    response_text = data[0].get("output", "")
                elif isinstance(data, dict):
                    response_text = data.get(
                        "output", data.get("response", data.get("message", ""))
                    )
                else:
                    response_text = str(data)

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                response_text = "Sorry, I received an invalid response format."

        elif "text/html" in content_type:
            # Handle HTML response (iframe format)
            html_content = response.text
            logger.info(f"HTML Webhook response received")

            # Extract message from iframe srcdoc attribute
            srcdoc_match = re.search(r'srcdoc="([^"]*)"', html_content)
            if srcdoc_match:
                response_text = (
                    srcdoc_match.group(1).replace("&quot;", '"').replace("&amp;", "&")
                )
                logger.info(f"Extracted message from HTML: {response_text[:100]}...")
            else:
                response_text = (
                    "I received your message but couldn't parse the response."
                )

        else:
            # Handle plain text or other formats
            response_text = response.text
            logger.info(f"Plain text response: {response_text[:100]}...")

        return {
            "success": True,
            "content": response_text
            or "I received your message, but I'm not sure how to respond right now.",
            "raw_response": response.text,
            "content_type": content_type,
        }

    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return {
            "success": False,
            "content": "Sorry, the request timed out. Please try again.",
            "error": "timeout",
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return {
            "success": False,
            "content": "Sorry, I'm having trouble connecting right now. Please try again later.",
            "error": str(e),
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "success": False,
            "content": "An unexpected error occurred. Please try again.",
            "error": str(e),
        }


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    return timestamp.strftime("%H:%M")


def display_chat_message(message: Dict[str, Any], message_key: str):
    """Display a single chat message"""
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", datetime.now())

    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(content)
            st.caption(f"You • {format_timestamp(timestamp)}")
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(content)
            st.caption(f"TROOPERS Assistant • {format_timestamp(timestamp)}")


def main():
    """Main application function"""
    initialize_session_state()

    # Minimal header
    st.markdown(
        """
    <div class="troopers-header">
        <h1 class="troopers-title">TROOPERS Assistant</h1>
        <p class="troopers-subtitle">Part-Time & Manpower Solutions</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Minimal session info (only show if debug mode or needed)
    if st.session_state.get("show_session_info", False):
        st.markdown(
            f"""
        <div class="session-info">
            Session: {st.session_state.session_id[:12]}... • {"Processing" if st.session_state.is_loading else "Ready"}
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        display_chat_message(message, f"message_{i}")

    # Show minimal loading spinner
    if st.session_state.is_loading:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                """
                <div class="minimal-spinner">
                    <div class="spinner"></div>
                    Thinking...
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Chat input
    if prompt := st.chat_input(
        "Ask about part-time jobs, hiring, or anything else...",
        disabled=st.session_state.is_loading,
    ):
        # Add user message to chat
        user_message = {"role": "user", "content": prompt, "timestamp": datetime.now()}
        st.session_state.messages.append(user_message)

        # Display user message immediately
        display_chat_message(
            user_message, f"user_message_{len(st.session_state.messages) - 1}"
        )

        # Set loading state
        st.session_state.is_loading = True
        st.rerun()

    # Process the latest user message if loading
    if st.session_state.is_loading and st.session_state.messages:
        latest_message = st.session_state.messages[-1]
        if latest_message["role"] == "user":
            # Send message to webhook
            response = send_message_to_webhook(
                latest_message["content"], st.session_state.session_id
            )

            # Add assistant response to chat
            assistant_message = {
                "role": "assistant",
                "content": response["content"],
                "timestamp": datetime.now(),
            }
            st.session_state.messages.append(assistant_message)

            # Clear loading state
            st.session_state.is_loading = False
            st.rerun()

    # Minimal sidebar
    with st.sidebar:
        st.markdown("**Chat Stats**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Sent",
                len([m for m in st.session_state.messages if m["role"] == "user"]),
                label_visibility="collapsed",
            )
        with col2:
            st.metric(
                "Received",
                len([m for m in st.session_state.messages if m["role"] == "assistant"]),
                label_visibility="collapsed",
            )

        st.markdown("---")

        # Actions in a cleaner layout
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear", type="secondary", use_container_width=True):
                st.session_state.messages = [st.session_state.messages[0]]
                st.rerun()
        with col2:
            if st.button("New Session", type="secondary", use_container_width=True):
                st.session_state.session_id = (
                    f"session_{int(time.time())}_{str(uuid.uuid4())[:8]}"
                )
                st.session_state.messages = [st.session_state.messages[0]]
                st.rerun()

        # Toggle session info display
        st.session_state.show_session_info = st.checkbox(
            "Show session info", value=False
        )

        # Minimal debug section
        with st.expander("Debug", expanded=False):
            st.text(
                f"Status: {'🟡 Processing' if st.session_state.is_loading else '🟢 Ready'}"
            )
            st.text(f"Session: {st.session_state.session_id[:16]}...")

            if st.button("Test Connection", type="secondary", use_container_width=True):
                test_response = send_message_to_webhook(
                    "Connection test", st.session_state.session_id
                )
                st.success("✅ Connected" if test_response["success"] else "❌ Failed")

            if st.session_state.messages:
                st.text("Latest:")
                st.json(st.session_state.messages[-1], expanded=False)


if __name__ == "__main__":
    main()
