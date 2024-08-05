from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True,)

    def __str__(self: Position) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True,)

    def __str__(self: TaskType) -> str:
        return self.name


class TaskPriority(models.Model):
    importance = models.PositiveSmallIntegerField(unique=True,)
    name = models.CharField(max_length=255, unique=True,)

    class Meta:
        ordering = ["importance"]

    def __str__(self: TaskPriority) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers"
    )

    def get_absolute_url(self: Worker) -> str:
        return reverse("task_manager:worker-detail", kwargs={"pk": self.pk})

    def __str__(self: Worker) -> str:
        return f"{self.username}  ({self.position})"


class Task(models.Model):
    IS_COMPLETED_CHOICES = (
        (True, "Yes"),
        (False, "No"),
    )

    name = models.CharField(max_length=255, unique=True,)
    description = models.TextField(max_length=255, blank=True, null=True,)
    deadline = models.DateField()
    is_completed = models.BooleanField(
        default=False,
        choices=IS_COMPLETED_CHOICES,
    )
    priority = models.ForeignKey(
        TaskPriority,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True
    )

    def __str__(self: Task) -> str:
        return (f"{self.name} (Type: {self.task_type}, "
                f"Priority: {self.priority}, Deadline: {self.deadline})")
