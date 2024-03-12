# payments/views.py
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ValidationError
from accounts.models import CustomUser

from .models import Project
from .serializers import *
from .helpers import *
from taskify.permissions import check_permission
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.select_related("created_by")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    paginate_by = 20

    def list(self, request, *args, **kwargs):
        print(CustomUser.objects.all(), request.user)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        result = check_permission(user)
        if result == "error":
            raise ValidationError({"detail": "Specify role for user to access data"})

        queryset = Project.objects.select_related(
            "created_by",
        )
        return queryset


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.select_related("project")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def list(self, request, *args, **kwargs):
        print(CustomUser.objects.all(), request.user)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        result = check_permission(user)
        if result == "error":
            raise ValidationError({"detail": "Specify role for user to access data"})

        queryset = Task.objects.select_related(
            "project",
        )
        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Perform permission checks for DELETE request
        if self.request.method == "DELETE":
            task = self.get_object()
            if task.created_by != user:
                raise PermissionDenied("You can only delete tasks created by you")

        return queryset

    def perform_destroy(self, instance):
        instance.delete()


class GetTaskByProjectView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    paginate_by = 20

    def list(self, request, *args, **kwargs):
        project_id = self.kwargs.get("pk")
        print("herery........", project_id)
        queryset = self.get_queryset().filter(project__id=project_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetTaskByMembersView(generics.ListAPIView):
    serializer_class = TaskMemberSerializer
    queryset = TaskMembers.objects.all()

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    paginate_by = 20

    def list(self, request, *args, **kwargs):
        task_id = self.kwargs.get("pk")
        queryset = self.get_queryset().filter(task__id=task_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskMembersListView(generics.ListCreateAPIView):
    serializer_class = TaskMemberSerializer
    queryset = TaskMembers.objects.all()

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    paginate_by = 20

    def perform_create(self, serializer):
        request_body = self.request.data
        if task := TaskMembers.objects.get(
            task__id=request_body["task"], member=request_body["member"]
        ):
            raise ValidationError(f"User already a member")
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            return TaskMemberResponseSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class TaskMembersListView(generics.RetrieveDestroyAPIView):
    queryset = TaskMembers.objects.all()
    serializer_class = TaskMemberSerializer
    permission_classes = [IsAuthenticated]


class TeamMembersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    paginate_by = 20
