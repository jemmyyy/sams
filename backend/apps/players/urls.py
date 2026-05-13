from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet

router = DefaultRouter()
router.register(r'', PlayerViewSet)

app_name = 'players'

urlpatterns = [
    path('', include(router.urls)),
]
