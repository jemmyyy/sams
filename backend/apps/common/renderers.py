from rest_framework.renderers import JSONRenderer


class StandardizedJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        is_success = status_code < 400

        message = ""
        if isinstance(data, dict):
            message = data.get("detail", "")

        response = {
            "success": is_success,
            "data": data if is_success else None,
            "errors": data if not is_success else None,
            "message": message,
        }

        return super().render(response, accepted_media_type, renderer_context)
