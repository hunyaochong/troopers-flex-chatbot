# TROOPERS Chatbot - Streamlit Interface

A Streamlit-based chat interface that connects to the TROOPERS AI agent running on n8n.

## Features

- 💬 Real-time chat interface
- 🔄 Connection to n8n webhook
- 📊 Chat statistics and session management
- 🎨 Professional TROOPERS branding
- 🐛 Debug mode for troubleshooting
- ⚡ Retry logic for reliable connections
- 📱 Responsive design

## Setup Instructions

### 1. Install Dependencies

```bash
cd troopers-flex-chatbot
pip install -r requirements.txt
```

### 2. Configuration

The app is pre-configured with your webhook URL:
```
https://primary-production-6654.up.railway.app/webhook/f1deda52-3942-419c-879b-5b8b0f28743e
```

To change the webhook URL, you can either:
- Set the `N8N_WEBHOOK_URL` environment variable
- Modify the `WEBHOOK_URL` in `config.py`

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Project Structure

```
troopers-flex-chatbot/
├── app.py              # Main Streamlit application
├── chat_utils.py       # Utility functions for chat operations
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Usage

1. **Start Chatting**: Type your message in the chat input at the bottom
2. **View Statistics**: Check the sidebar for chat metrics
3. **Clear Chat**: Use the "Clear Chat" button to reset the conversation
4. **New Session**: Start a fresh session with a new session ID
5. **Debug Mode**: Enable in the sidebar to view technical details

## API Integration

The app sends POST requests to your n8n webhook with this format:

```json
{
  "message": "User's message",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "sessionId": "session_1704110400_abc12345"
}
```

Expected response format from n8n:
```json
[
  {
    "output": "AI agent's response message"
  }
]
```

## Customization

### Styling
Modify the CSS in `app.py` or `config.py` to change the appearance.

### Webhook Configuration
Update `config.py` to change webhook settings, timeouts, and retry logic.

### Chat Behavior
Modify `chat_utils.py` to change message processing and validation.

## Troubleshooting

1. **Connection Issues**: Check the webhook URL and ensure n8n is running
2. **Timeout Errors**: Increase `timeout_seconds` in `config.py`
3. **Debug Information**: Enable debug mode in the sidebar
4. **Logs**: Check the console output for detailed error information

## Environment Variables

- `N8N_WEBHOOK_URL`: Override the default webhook URL

## License

This project is part of the TROOPERS ecosystem. # troopers-flex-chatbot
