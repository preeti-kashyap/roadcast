from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import FriendRequest


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'email', 'password', 'full_name', 'date_of_birth']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = get_user_model().objects.create_user(**validated_data)
#         return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'full_name', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


# class EmailAuthTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField(label="Email")
#     password = serializers.CharField(
#         label="Password",
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         if email and password:
#             user = authenticate(request=self.context.get('request'), email=email, password=password)

#             if not user:
#                 msg = 'Unable to log in with provided credentials.'
#                 raise serializers.ValidationError(msg, code='authorization')

#         else:
#             msg = 'Must include "email" and "password".'
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
#         return attrs

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

