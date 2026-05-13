from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CancellationRequestViewSet

router = DefaultRouter()
router.register(r'', CancellationRequestViewSet)

app_name = 'cancellations'

urlpatterns = [
    path('', include(router.urls)),
]
