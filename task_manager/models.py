from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True,)

    def __str__(self: Position) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True,)

    def __str__(self: TaskType) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self: Worker) -> str:
        return f"{self.username} – {self.position}"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
        ("Optional", "Optional"),
    )

    name = models.CharField(max_length=255, unique=True,)
    description = models.TextField(blank=True, null=True,)
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False,)
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks", blank=True)

    def __str__(self: Task) -> str:
        return (f"{self.name} (Type: {self.task_type}, "
                f"Priority: {self.priority}, Deadline: {self.deadline})")
