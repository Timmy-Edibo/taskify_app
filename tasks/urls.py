# accounts/urls.py
from django.urls import path
from .views import *

# administrator
urlpatterns = [
    path("projects", ProjectListView.as_view(), name="list-create-project-view"),
    path("projects/<int:pk>", ProjectDetailView.as_view(), name="project-detail-view"),
    path(
        "tasks/<int:pk>/members/",
        GetTaskByProjectView.as_view(),
        name="taskmembers-list-view",
    ),
    path("tasks", TaskListView.as_view(), name="list-create-task-view"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail-view"),
    path(
        "tasks/task-members/",
        TaskMembersListView.as_view(),
        name="taskmembers-list-view",
    ),
    path(
        "team-members/",
        TeamMembersView.as_view(),
        name="team-member-list-view",
    ),
]
