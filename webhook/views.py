import json
import logging
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import WhatsAppMessage, WhatsAppCall
from .serializers import WhatsAppWebhookSerializer

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    """
    WhatsApp webhook endpoint.
    
    GET: Webhook verification (required by Meta)
    POST: Receive incoming messages
    """
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return HttpResponse(challenge, content_type='text/plain')
        else:
            logger.warning(f"Webhook verification failed. Mode: {mode}, Token match: {token == settings.WHATSAPP_VERIFY_TOKEN}")
            return HttpResponse('Verification failed', status=403)
    
    elif request.method == 'POST':
        # Handle incoming messages
        try:
            data = json.loads(request.body)
            logger.info(f"Received webhook payload: {json.dumps(data, indent=2)}")
            
            # Verify it's a WhatsApp Business Account webhook
            if data.get('object') != 'whatsapp_business_account':
                logger.warning(f"Invalid webhook object type: {data.get('object')}")
                return JsonResponse({'status': 'error', 'message': 'Invalid webhook object'}, status=400)
            
            # Process each entry
            entries = data.get('entry', [])
            processed_messages = []
            processed_calls = []
            
            for entry in entries:
                changes = entry.get('changes', [])
                
                for change in changes:
                    value = change.get('value', {})
                    field = change.get('field')
                    
                    # Handle messages
                    if field == 'messages':
                        messages = value.get('messages', [])
                        contacts = value.get('contacts', [])
                        metadata = value.get('metadata', {})
                        
                        # Create a mapping of wa_id to contact info
                        contact_map = {contact.get('wa_id'): contact for contact in contacts}
                        
                        # Process each message
                        for message in messages:
                            message_data = process_message(message, contact_map, metadata, entry.get('id'))
                            if message_data:
                                processed_messages.append(message_data)
                    
                    # Handle calls
                    elif field == 'calls':
                        calls = value.get('calls', [])
                        contacts = value.get('contacts', [])
                        metadata = value.get('metadata', {})
                        
                        # Create a mapping of wa_id to contact info
                        contact_map = {contact.get('wa_id'): contact for contact in contacts}
                        
                        # Process each call event
                        for call in calls:
                            call_data = process_call(call, contact_map, metadata)
                            if call_data:
                                processed_calls.append(call_data)
            
            response_data = {
                'status': 'success',
                'messages_processed': len(processed_messages),
                'calls_processed': len(processed_calls),
            }
            
            if processed_messages:
                response_data['message_ids'] = [msg.message_id for msg in processed_messages]
            if processed_calls:
                response_data['call_ids'] = [call.call_id for call in processed_calls]
            
            return JsonResponse(response_data, status=200)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def process_message(message, contact_map, metadata, entry_id):
    """
    Process a single message from the webhook payload and save it to the database.
    
    Args:
        message: The message object from the webhook
        contact_map: Dictionary mapping wa_id to contact information
        metadata: Metadata containing phone_number_id and display_phone_number
        entry_id: The entry ID from the webhook
    
    Returns:
        WhatsAppMessage instance if created successfully, None otherwise
    """
    try:
        from_number = message.get('from')
        message_id = message.get('id')
        message_type = message.get('type')
        timestamp = message.get('timestamp')
        
        # Get contact information
        contact = contact_map.get(from_number, {})
        contact_name = contact.get('profile', {}).get('name', '')
        wa_id = contact.get('wa_id', from_number)
        
        # Extract message content based on type
        message_text = None
        audio_id = None
        audio_url = None
        audio_mime_type = None
        is_voice = False

        # Initialize new message type fields
        image_id = None
        image_url = None
        image_mime_type = None
        image_caption = None

        video_id = None
        video_url = None
        video_mime_type = None
        video_caption = None

        document_id = None
        document_url = None
        document_filename = None
        document_mime_type = None

        latitude = None
        longitude = None

        sticker_id = None
        sticker_url = None
        sticker_mime_type = None
        is_animated = False

        contacts_data = None

        if message_type == 'text':
            message_text = message.get('text', {}).get('body', '')
        elif message_type == 'audio':
            audio_data = message.get('audio', {})
            audio_id = audio_data.get('id')
            audio_url = audio_data.get('url')
            audio_mime_type = audio_data.get('mime_type')
            is_voice = audio_data.get('voice', False)
        elif message_type == 'image':
            image_data = message.get('image', {})
            image_id = image_data.get('id')
            image_url = image_data.get('url')
            image_mime_type = image_data.get('mime_type')
            image_caption = image_data.get('caption')
        elif message_type == 'video':
            video_data = message.get('video', {})
            video_id = video_data.get('id')
            video_url = video_data.get('url')
            video_mime_type = video_data.get('mime_type')
            video_caption = video_data.get('caption')
        elif message_type == 'document':
            doc_data = message.get('document', {})
            document_id = doc_data.get('id')
            document_url = doc_data.get('url')
            document_filename = doc_data.get('filename')
            document_mime_type = doc_data.get('mime_type')
        elif message_type == 'location':
            location_data = message.get('location', {})
            latitude = location_data.get('latitude')
            longitude = location_data.get('longitude')
        elif message_type == 'sticker':
            sticker_data = message.get('sticker', {})
            sticker_id = sticker_data.get('id')
            sticker_url = sticker_data.get('url')
            sticker_mime_type = sticker_data.get('mime_type')
            is_animated = sticker_data.get('animated', False)
        elif message_type == 'contacts':
            contacts_data = message.get('contacts', [])
        
        # Create or update message record
        message_obj, created = WhatsAppMessage.objects.update_or_create(
            message_id=message_id,
            defaults={
                'wa_id': wa_id,
                'from_number': from_number,
                'contact_name': contact_name,
                'message_type': message_type,
                'message_text': message_text,
                'audio_id': audio_id,
                'audio_url': audio_url,
                'audio_mime_type': audio_mime_type,
                'is_voice': is_voice,
                'image_id': image_id,
                'image_url': image_url,
                'image_mime_type': image_mime_type,
                'image_caption': image_caption,
                'video_id': video_id,
                'video_url': video_url,
                'video_mime_type': video_mime_type,
                'video_caption': video_caption,
                'document_id': document_id,
                'document_url': document_url,
                'document_filename': document_filename,
                'document_mime_type': document_mime_type,
                'latitude': latitude,
                'longitude': longitude,
                'sticker_id': sticker_id,
                'sticker_url': sticker_url,
                'sticker_mime_type': sticker_mime_type,
                'is_animated': is_animated,
                'contacts_data': contacts_data,
                'timestamp': timestamp,
                'phone_number_id': metadata.get('phone_number_id', ''),
                'display_phone_number': metadata.get('display_phone_number', ''),
                'raw_payload': message,  # Store the complete message payload
            }
        )
        
        if created:
            logger.info(f"New message saved: {message_id} from {from_number} ({message_type})")
        else:
            logger.info(f"Message updated: {message_id}")
        
        # Here you can add your chatbot logic to process the message
        # For example, you could trigger an async task or call a function
        # handle_message_response(message_obj)
        
        return message_obj
        
    except Exception as e:
        logger.error(f"Error processing individual message: {str(e)}", exc_info=True)
        return None


def process_call(call, contact_map, metadata):
    """
    Process a single call event from the webhook payload and save it to the database.
    Each event (connect, terminate) is stored as a separate record.
    
    Args:
        call: The call object from the webhook
        contact_map: Dictionary mapping wa_id to contact information
        metadata: Metadata containing phone_number_id and display_phone_number
    
    Returns:
        WhatsAppCall instance if created successfully, None otherwise
    """
    try:
        call_id = call.get('id')
        from_number = call.get('from')
        to_number = call.get('to')
        event = call.get('event')
        direction = call.get('direction')
        timestamp = call.get('timestamp')
        
        # Get contact information
        contact = contact_map.get(from_number, {})
        contact_name = contact.get('profile', {}).get('name', '')
        wa_id = contact.get('wa_id', from_number)
        
        # Call timing (available on terminate/completed events)
        call_status = call.get('status')
        start_time = call.get('start_time')
        end_time = call.get('end_time')
        duration = call.get('duration')
        
        # Session data (available on connect events for WebRTC)
        session = call.get('session', {})
        session_sdp = session.get('sdp')
        session_sdp_type = session.get('sdp_type')
        
        # Create call record (each event as separate record)
        call_obj = WhatsAppCall.objects.create(
            call_id=call_id,
            from_number=from_number,
            to_number=to_number,
            wa_id=wa_id,
            contact_name=contact_name,
            event=event,
            direction=direction,
            status=call_status,
            timestamp=timestamp,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            session_sdp=session_sdp,
            session_sdp_type=session_sdp_type,
            phone_number_id=metadata.get('phone_number_id', ''),
            display_phone_number=metadata.get('display_phone_number', ''),
            raw_payload=call,
        )
        
        logger.info(f"Call event saved: {call_id} | {event} | from {from_number} to {to_number}")
        
        # Here you can add logic to handle calls programmatically
        # For example: handle_call_event(call_obj)
        
        return call_obj
        
    except Exception as e:
        logger.error(f"Error processing call event: {str(e)}", exc_info=True)
        return None
