from rest_framework.renderers import JSONRenderer

class StandardizedJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        
        response = {
            "success": status_code < 400,
            "data": data if status_code < 400 else None,
            "errors": data if status_code >= 400 else None,
            "message": data.get("detail", "") if isinstance(data, dict) and "detail" in data else ""
        }
        
        return super().render(response, accepted_media_type, renderer_context)
