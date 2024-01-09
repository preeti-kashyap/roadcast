from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserSearchSerializer, FriendRequestSerializer, FriendListSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import FriendRequest       
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key, 'user_id': token.user_id}, status=status.HTTP_201_CREATED, headers=headers)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(UserLoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})


    def get_object(self):
        return self.request.user

    
# class UserLoginView(ObtainAuthToken):
#     serializer_class = EmailAuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)

class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = UserSearchPagination  # Use the custom pagination class

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search', '')

        # Check if the search keyword is an exact email match
        exact_email_match = get_user_model().objects.filter(email__iexact=search_keyword).first()
        if exact_email_match:
            return [exact_email_match]  # Return a single user instance as a list

        # Otherwise, search by various fields containing the keyword
        return get_user_model().objects.filter(
            Q(username__icontains=search_keyword) |
            Q(full_name__icontains=search_keyword) |
            Q(first_name__icontains=search_keyword) |
            Q(last_name__icontains=search_keyword)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendRequestCreateView(APIView):
    # @method_decorator(csrf_exempt)
    # @ratelimit(key='user', rate='3/m', block=True)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
    # @method_decorator(ratelimit(key='user', rate='3/m', block=True))
    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')  
        from_user = self.request.user
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user_id=to_user_id, status='pending')

        serializer = FriendRequestSerializer(friend_request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendRequestUpdateView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get('action')

        if action == 'accept':
            instance.status = 'accepted'
            instance.save()
            return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)

        elif action == 'reject':
            instance.status = 'rejected'
            instance.save()
            return Response({'detail': 'Friend request rejected'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

class PendingFriendRequestsListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')

class FriendListView(generics.ListAPIView):
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_requests = FriendRequest.objects.filter(from_user=user, status='accepted')
        return friend_requests