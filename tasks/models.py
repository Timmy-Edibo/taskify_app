from typing import Iterable
from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField()
    task_count = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task_identifier = models.IntegerField(
        unique=True, null=True, blank=True, editable=False
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/images", null=True, blank=True)
    date_added = models.DateTimeField()
    date_due = models.DateTimeField()
    status = models.IntegerField()

    def save(self, *args, **kwargs):
        identifier = Task.objects.last().id + 1

        if not self.task_identifier:
            self.task_identifier = identifier
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class TaskMembers(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.name
