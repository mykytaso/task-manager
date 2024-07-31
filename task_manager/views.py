from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import TaskForm, TaskSearchForm, WorkerSearchForm
from .models import Worker, Task, TaskType, Position


@login_required
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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        order = self.request.GET.get("order", "username")
        queryset = Worker.objects.select_related("position").annotate(Count("tasks")).order_by(order)

        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        order = self.request.GET.get("order", "name")
        queryset = Task.objects.select_related(
            "priority",
            "task_type",
        ).prefetch_related(
            "assignees",
        ).annotate(
            Count("assignees")
        ).order_by(
            order
        )

        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        assigned_workers = context["object"].assignees.all()
        context["not_assigned_workers"] = Worker.objects.exclude(id__in=assigned_workers.values_list('id', flat=True))
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    ordering = "name"


class TaskTypeCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:tasktype-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    ordering = "name"


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


@login_required
def assign_unassign(request):
    if request.method == "POST":
        task = get_object_or_404(
            Task,
            id=request.POST.get("task_id", ""),
        )
        worker = get_object_or_404(
            Worker,
            id=request.POST.get("worker_id", ""),
        )

        if worker in task.assignees.all():
            task.assignees.remove(worker)
        else:
            task.assignees.add(worker)

        if "worker" in request.get_full_path():
            return redirect(reverse('task_manager:task-detail', args=[task.id]))
        if "task" in request.get_full_path():
            return redirect(reverse('task_manager:worker-detail', args=[worker.id]))

    raise Http404("assign_unassign_worker view error")
