from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerRatingViewSet

router = DefaultRouter()
router.register(r'', PlayerRatingViewSet)

app_name = 'ratings'

urlpatterns = [
    path('', include(router.urls)),
]
