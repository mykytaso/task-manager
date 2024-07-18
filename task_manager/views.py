from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Worker, Task, TaskType, Position


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
        "num_positions": num_positions
    }
    return render(request, "task_manager/index.html", context=context)


class WorkerListView(generic.ListView):
    model = Worker


class WorkerDetailView(generic.DetailView):
    model = Worker


class TaskListView(generic.ListView):
    model = Task


class TaskDetailView(generic.DetailView):
    model = Task


class TaskTypeListView(generic.ListView):
    model = TaskType


class PositionListView(generic.ListView):
    model = Position

