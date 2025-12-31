from django.contrib import admin
from .models import WhatsAppMessage, WhatsAppCall


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['from_number', 'contact_name', 'message_type', 'message_text', 'created_at', 'processed']
    list_filter = ['message_type', 'processed', 'created_at']
    search_fields = ['from_number', 'contact_name', 'message_text', 'message_id']
    readonly_fields = ['message_id', 'wa_id', 'from_number', 'contact_name', 'message_type', 
                      'message_text', 'audio_id', 'audio_url', 'audio_mime_type', 'is_voice',
                      'timestamp', 'phone_number_id', 'display_phone_number', 'raw_payload', 'created_at']
    
    def has_add_permission(self, request):
        return False  # Messages are only created via webhook


@admin.register(WhatsAppCall)
class WhatsAppCallAdmin(admin.ModelAdmin):
    list_display = ['from_number', 'to_number', 'contact_name', 'event', 'status', 'direction', 'duration', 'created_at']
    list_filter = ['event', 'status', 'direction', 'created_at']
    search_fields = ['from_number', 'to_number', 'contact_name', 'call_id']
    readonly_fields = ['call_id', 'from_number', 'to_number', 'wa_id', 'contact_name', 
                      'event', 'direction', 'status', 'timestamp', 'start_time', 'end_time',
                      'duration', 'session_sdp', 'session_sdp_type', 'phone_number_id',
                      'display_phone_number', 'raw_payload', 'created_at']
    
    def has_add_permission(self, request):
        return False  # Calls are only created via webhook
