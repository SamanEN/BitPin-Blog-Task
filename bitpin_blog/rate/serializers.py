from rest_framework import serializers
from .models import Rate

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'user', 'blog', 'rating', 'created_at']
        read_only_fields = ['created_at', 'user']
