from apps.permissions.permissions import IsCoach, IsOperations
from rest_framework import viewsets

from .models import PlayerRating
from .serializers import PlayerRatingSerializer


class PlayerRatingViewSet(viewsets.ModelViewSet):
    queryset = PlayerRating.objects.all()
    serializer_class = PlayerRatingSerializer
    permission_classes = [IsCoach | IsOperations]

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user)
