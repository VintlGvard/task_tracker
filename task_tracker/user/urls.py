from django.urls import path
from .views import RegisterView, UserProfileView, UserListView, CustomTokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('users/', UserListView.as_view()),
]
