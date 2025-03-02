from django.urls import path
from .views import TaskListCreateView, TaskDetailView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access + refresh tokens
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh access token
    path('logout/', LogoutView.as_view(), name='auth_logout'),  # Blacklist refresh token
]
