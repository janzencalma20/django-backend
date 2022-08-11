from core.user.models import CohereUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CohereUser
        fields = ['id', 'username', 'email', 'is_active', 'created', 'updated']
        read_only_field = ['is_active']
