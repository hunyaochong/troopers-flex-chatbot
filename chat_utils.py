"""Utility functions for the TROOPERS chatbot"""

import requests
import json
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from config import WEBHOOK_URL, CHAT_CONFIG

logger = logging.getLogger(__name__)


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return f"session_{int(time.time())}_{str(uuid.uuid4())[:8]}"


def send_message_to_webhook(
    message: str, session_id: str, max_retries: int = 3
) -> Dict[str, Any]:
    """
    Send message to n8n webhook with retry logic

    Args:
        message: User message to send
        session_id: Unique session identifier
        max_retries: Number of retry attempts

    Returns:
        Dictionary with response data
    """
    payload = {
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "sessionId": session_id,
    }

    headers = {"Content-Type": "application/json"}

    for attempt in range(max_retries):
        try:
            logger.info(f"Sending message (attempt {attempt + 1}): {message}")

            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                headers=headers,
                timeout=CHAT_CONFIG["timeout_seconds"],
            )

            response.raise_for_status()
            data = response.json()

            logger.info(f"Webhook response: {data}")

            # Parse response based on n8n output format
            response_text = parse_webhook_response(data)

            return {
                "success": True,
                "content": response_text,
                "raw_response": data,
                "attempt": attempt + 1,
            }

        except requests.exceptions.Timeout:
            logger.warning(f"Request timeout on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                return {
                    "success": False,
                    "content": "Sorry, the request timed out. Please try again.",
                    "error": "timeout",
                    "attempt": attempt + 1,
                }
            time.sleep(1)  # Brief delay before retry

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return {
                    "success": False,
                    "content": "Sorry, I'm having trouble connecting right now. Please try again later.",
                    "error": str(e),
                    "attempt": attempt + 1,
                }
            time.sleep(1)  # Brief delay before retry

        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            return {
                "success": False,
                "content": "An unexpected error occurred. Please try again.",
                "error": str(e),
                "attempt": attempt + 1,
            }

    return {
        "success": False,
        "content": "Failed to get response after multiple attempts.",
        "error": "max_retries_exceeded",
    }


def parse_webhook_response(data: Any) -> str:
    """
    Parse the webhook response to extract the message content

    Args:
        data: Raw response data from webhook

    Returns:
        Extracted message content
    """
    # Handle array response from n8n (your example format)
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict) and "output" in first_item:
            return first_item["output"]

    # Handle direct dictionary response
    if isinstance(data, dict):
        for key in ["output", "response", "message", "content"]:
            if key in data:
                return data[key]

    # Fallback to string representation
    response_text = str(data)
    return (
        response_text
        if response_text and response_text != "None"
        else "I received your message, but I'm not sure how to respond right now."
    )


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display in chat"""
    return timestamp.strftime("%H:%M")


def validate_message(message: str) -> bool:
    """Validate user message before sending"""
    if not message or not message.strip():
        return False
    if len(message.strip()) > 5000:  # Reasonable message length limit
        return False
    return True


def create_message_dict(
    role: str, content: str, timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """Create a standardized message dictionary"""
    return {"role": role, "content": content, "timestamp": timestamp or datetime.now()}


def get_chat_statistics(messages: list) -> Dict[str, int]:
    """Calculate chat statistics from message list"""
    return {
        "total_messages": len(messages),
        "user_messages": len([m for m in messages if m["role"] == "user"]),
        "assistant_messages": len([m for m in messages if m["role"] == "assistant"]),
        "conversation_length": len(messages) - 1,  # Excluding welcome message
    }
