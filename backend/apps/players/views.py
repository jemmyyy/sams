from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.permissions.permissions import IsOperations
from ..models import Player
from ..serializers import PlayerSerializer
from ..services import PlayerService

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsOperations]
    filterset_fields = ['first_name', 'last_name', 'registration_number']
    search_fields = ['first_name', 'last_name', 'registration_number']

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        count = PlayerService.bulk_import_from_csv(request.user.academy, csv_file)
        return Response({"message": f"Successfully imported {count} players"}, status=status.HTTP_201_CREATED)
