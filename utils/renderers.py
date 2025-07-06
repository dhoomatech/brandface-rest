from rest_framework.renderers import JSONRenderer
from utils.encrypt_utils import encrypt_response

class ConditionalEncryptedJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get('request')
        view = renderer_context.get('view')

        if getattr(getattr(view, 'get_view_name', lambda: None), 'encrypt_response', False) \
            or getattr(view, 'encrypt_response', False) \
            or getattr(getattr(view, 'get_view', lambda: None), 'encrypt_response', False):
            # Encrypt if explicitly marked
            raw = JSONRenderer().render(data).decode()
            encrypted = encrypt_response(raw)
            return super().render({'encrypted_data': encrypted}, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)
