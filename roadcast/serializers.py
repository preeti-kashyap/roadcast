from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'full_name', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'full_name']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

class FriendListSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField(source='to_user.id')
    friend_username = serializers.CharField(source='to_user.username')
    friend_full_name = serializers.CharField(source='to_user.full_name', allow_null=True)
    status = serializers.CharField()

