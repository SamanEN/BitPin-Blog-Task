from rest_framework import serializers
from .models import Rate

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'user', 'blog', 'rating', 'created_at']
        read_only_fields = ['created_at', 'user']

    def validate(self, data):
        """
        Prevent a user from rating the same blog more than once.
        """
        user = self.context['request'].user
        blog = data['blog']

        if Rate.objects.filter(user=user, blog=blog).exists():
            raise serializers.ValidationError("You have already rated this blog.")
        return data
