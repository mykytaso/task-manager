from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True,)


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True,)


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
    )


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True,)
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
    )
