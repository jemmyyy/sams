from rest_framework import serializers
from ..models import PlayerRating

class PlayerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRating
        fields = '__all__'
        read_only_fields = ('academy', 'coach')
