from rest_framework import generics, filters
from .models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response


class LogoutView(APIView):
    """
    Handles user logout by blacklisting the provided refresh token.

    Methods:
    -------
    post(request):
        Invalidates the provided refresh token by adding it to the blacklist.
        Returns a success message if the token is blacklisted successfully,
        otherwise returns an error message.

    Parameters:
    ----------
    request : Request
        The HTTP request object containing the refresh token in the request data.

    Returns:
    -------
    Response
        A Response object with a success message and status code 200 if the token
        is blacklisted successfully, or an error message and status code 400 if
        there is an issue with the provided token or any other exception occurs.
    """
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Adds the token’s "jti" to the blacklist
            return Response({"detail": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class TaskListCreateView(generics.ListCreateAPIView):
    """
    TaskListCreateView is a view that provides both list and create functionalities for Task objects.

    Attributes:
    -----------
        queryset (QuerySet): The base queryset for retrieving Task objects.
        serializer_class (Serializer): The serializer class used for Task objects.
        filter_backends (list): A list of filter backends used for filtering, searching, and ordering.
        search_fields (list): A list of fields that can be searched.
        ordering_fields (list): A list of fields that can be used for ordering.
        filterset_fields (list): A list of fields that can be used for filtering.

    Methods:
    --------
        get_queryset(self):
            Returns a queryset of Task objects that belong to the authenticated user.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'completed']
    filterset_fields = ['completed']

    def get_queryset(self):
            # Only return tasks belonging to the authenticated user
            return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated user
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    TaskDetailView is a view that provides retrieve, update, and destroy actions for Task instances.

    This view ensures that only tasks owned by the authenticated user can be accessed or modified.

    Attributes:
    -----------
        serializer_class (TaskSerializer): The serializer class used to validate and serialize the Task instances.

    Methods:
    --------
        get_queryset(self):
            Returns a queryset of Task instances that are owned by the authenticated user.
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Only allow access to tasks owned by the authenticated user
        return Task.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        # Automatically set the user field to the authenticated user
        serializer.save(user=self.request.user)
        
    def perform_destroy(self, instance):
        # Ensure that only the owner can delete the task
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this task.")
