from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, FriendRequestCreateView, FriendRequestUpdateView, FriendRequestListView, PendingFriendRequestsListView, FriendListView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user-search/', UserSearchView.as_view(), name='user-search'),
    path('friend-requests/send/', FriendRequestCreateView.as_view(), name='send-friend-request'),
    path('friend-requests/<int:pk>/', FriendRequestUpdateView.as_view(), name='update-friend-request'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('friend-requests/pending/', PendingFriendRequestsListView.as_view(), name='pending-friend-requests'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
]
