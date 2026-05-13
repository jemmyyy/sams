from rest_framework.views import exception_handler
from rest_framework.response import Response

def standardized_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Standardized format is handled by the renderer
        pass
    else:
        # For unhandled exceptions
        response = Response({
            "detail": "An internal server error occurred."
        }, status=500)

    return response
