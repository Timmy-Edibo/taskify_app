from django.contrib import admin
from .models import *


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "task_count", "date_added", "due_date")
    search_fields = ("name", "created_by", "task_count", "date_added", "due_date")
    list_filter = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_identifier",
        "image",
        "date_added",
        "date_due",
        "project",
        "status",
    )
    list_filter = ("name",)


@admin.register(TaskMembers)
class TaskmemberAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "member",
    )
    list_filter = ("task",)
