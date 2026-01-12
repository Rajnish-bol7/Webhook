# WhatsApp Webhook for Django

A Django webhook application to receive and process WhatsApp Business API messages. This project handles incoming messages (text, audio, etc.) from WhatsApp and stores them in a database for chatbot processing.

## Features

- ✅ Webhook verification endpoint for Meta
- ✅ Handles text messages
- ✅ Handles audio/voice messages
- ✅ Stores messages in database with all metadata
- ✅ Extracts sender information, message type, and content
- ✅ Ready for chatbot integration

## Setup Instructions

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `WHATSAPP_VERIFY_TOKEN`: A random token you'll use for webhook verification in Meta

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

This allows you to view messages in Django admin.

### 5. Run the Development Server

```bash
python manage.py runserver
```

The webhook will be available at: `http://localhost:8000/webhook/`

## Configuring Meta (Facebook) Webhook

### 1. Set Webhook URL

In your Meta App Dashboard (https://developers.facebook.com/), navigate to:
- Your WhatsApp Business App
- Configuration → Webhook

Set the webhook URL to: `https://your-domain.com/webhook/`

### 2. Set Verify Token

- Enter the same token you set in your `.env` file as `WHATSAPP_VERIFY_TOKEN`
- Click "Verify and Save"

### 3. Subscribe to Webhook Fields

Subscribe to the `messages` field to receive incoming messages.

## Webhook Endpoint

### GET `/webhook/`
Used for webhook verification by Meta. Returns the challenge parameter when verification token matches.

**Query Parameters:**
- `hub.mode`: Should be "subscribe"
- `hub.verify_token`: Must match `WHATSAPP_VERIFY_TOKEN` in settings
- `hub.challenge`: Challenge string from Meta

### POST `/webhook/`
Receives incoming WhatsApp messages from Meta.

**Response:**
```json
{
  "status": "success",
  "messages_processed": 1,
  "message_ids": ["wamid.xxx"]
}
```

## Message Processing

### Supported Message Types

1. **Text Messages**
   - Extracts: `message_text`, `from_number`, `contact_name`, `timestamp`

2. **Audio/Voice Messages**
   - Extracts: `audio_id`, `audio_url`, `audio_mime_type`, `is_voice`, `timestamp`

### Database Model

Messages are stored in the `WhatsAppMessage` model with the following key fields:
- `message_id`: Unique WhatsApp message ID
- `from_number`: Sender's phone number
- `contact_name`: Sender's profile name
- `message_type`: Type of message (text, audio, image, etc.)
- `message_text`: Text content (for text messages)
- `audio_url`: Download URL (for audio messages)
- `raw_payload`: Complete message payload as JSON
- `processed`: Flag to track if message has been processed by chatbot

## Viewing Messages

### Django Admin

1. Start the server: `python manage.py runserver`
2. Visit: `http://localhost:8000/admin/`
3. Login with superuser credentials
4. View messages under "Webhook → WhatsApp Messages"

### Programmatic Access

```python
from webhook.models import WhatsAppMessage

# Get unprocessed messages
unprocessed = WhatsAppMessage.objects.filter(processed=False)

# Get latest messages from a specific user
messages = WhatsAppMessage.objects.filter(
    from_number='911234567890'
).order_by('-created_at')

# Process a message
for message in unprocessed:
    # Your chatbot logic here
    print(f"From: {message.from_number}")
    print(f"Message: {message.message_text}")
    print(f"Type: {message.message_type}")
    
    # Mark as processed
    message.processed = True
    message.save()
```

## Adding Chatbot Logic

To add your chatbot response logic, modify the `process_message` function in `webhook/views.py`. You can:

1. Check the message content
2. Generate a response
3. Send a reply using WhatsApp Business API
4. Mark the message as processed

Example:

```python
def handle_message_response(message_obj):
    """Example chatbot handler"""
    if message_obj.message_type == 'text':
        user_message = message_obj.message_text.lower()
        
        if 'hello' in user_message or 'hi' in user_message:
            # Send greeting response
            send_whatsapp_message(
                to=message_obj.from_number,
                message="Hello! How can I help you?"
            )
        
        message_obj.processed = True
        message_obj.save()
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Set proper `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Use a reverse proxy (nginx) with HTTPS
5. Set up proper logging
6. Use environment variables for all secrets

## Webhook Payload Structure

### Text Message
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "911234567890",
          "id": "wamid.xxx",
          "timestamp": "1766216432",
          "type": "text",
          "text": {"body": "Hello"}
        }]
      }
    }]
  }]
}
```

### Audio Message
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "911234567890",
          "id": "wamid.xxx",
          "timestamp": "1766216635",
          "type": "audio",
          "audio": {
            "id": "24950395794663592",
            "url": "https://lookaside.fbsbx.com/...",
            "mime_type": "audio/ogg; codecs=opus",
            "voice": true
          }
        }]
      }
    }]
  }]
}
```

## Troubleshooting

### Webhook Verification Fails
- Ensure `WHATSAPP_VERIFY_TOKEN` in `.env` matches the token in Meta Dashboard
- Check that the webhook URL is accessible (use ngrok for local testing)

### Messages Not Received
- Verify webhook is subscribed to "messages" field in Meta Dashboard
- Check server logs for errors
- Ensure the webhook endpoint is publicly accessible

### Database Errors
- Run migrations: `python manage.py migrate`
- Check database permissions

## License

This project is open source and available under the MIT License.

