from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import TaskForm, TaskSearchForm, WorkerSearchForm
from .models import Worker, Task, TaskType, Position
from django.db.models.functions import Lower


@login_required
def index(request):
    current_date = timezone.now().date()
    workers = Worker.objects.all()
    tasks = Task.objects.select_related(
        "priority",
        "task_type",
    ).prefetch_related("assignees",)
    num_tasks = tasks.count()
    num_finished_tasks = tasks.filter(is_completed=True).count()
    num_tasks_in_progress = tasks.filter(is_completed=False).count()

    task_types = TaskType.objects.all()
    positions = Position.objects.all()

    progress = round((100 / num_tasks) * num_finished_tasks)

    hot_task = tasks.filter(
        deadline__gte=current_date,
        is_completed=False
    ).order_by("deadline").first()

    missed_deadline = tasks.filter(
        deadline__lt=current_date,
        is_completed=False
    ).order_by("-deadline")

    context = {
        "workers": workers,
        "tasks": tasks,
        "num_tasks": num_tasks,
        "num_finished_tasks": num_finished_tasks,
        "num_tasks_in_progress": num_tasks_in_progress,
        "task_types": task_types,
        "positions": positions,
        "progress": progress,
        "hot_task": hot_task,
        "missed_deadline": missed_deadline,
    }
    return render(request, "task_manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "")

        context.update({
            "search_form": WorkerSearchForm(initial={"search": search}),
            "order_direction": "asc" if self.request.GET.get(
                "order_direction", "") == "desc" else "desc"
        })
        return context

    def get_queryset(self):
        order_type = self.request.GET.get("order", "username")
        order_direction = self.request.GET.get("order_direction", "asc")

        queryset = Worker.objects.select_related(
            "position"
        ).annotate(Count("tasks")).order_by(
            Lower(order_type).asc() if order_direction == "asc" else Lower(
                order_type).desc()
        )

        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["search"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search_form"] = TaskSearchForm(
            initial={"search": search}
        )
        context.update({
            "search_form": TaskSearchForm(initial={"search": search}),
            "order_direction": "asc" if self.request.GET.get(
                "order_direction", "") == "desc" else "desc"
        })
        return context

    def get_queryset(self):
        order_type = self.request.GET.get("order", "name")
        order_direction = self.request.GET.get("order_direction", "asc")

        queryset = Task.objects.select_related(
            "priority",
            "task_type",
        ).prefetch_related(
            "assignees",
        ).annotate(
            Count("assignees")
        ).order_by(
            Lower(order_type).asc() if order_direction == "asc" else Lower(
                order_type).desc()
        )

        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["search"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        assigned_workers = context["object"].assignees.all()
        context["not_assigned_workers"] = Worker.objects.exclude(
            id__in=assigned_workers.values_list("id", flat=True)
        )
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
def assign_unassign_worker(request):
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
        return redirect(request.POST.get("current_url"))

    raise Http404("assign_unassign_worker view error")


@login_required
def task_status_switch(request):
    if request.method == "POST":
        task = get_object_or_404(Task, id=request.POST.get("task_id", ""))
        task.is_completed = not task.is_completed
        task.save()
        return redirect(request.POST.get("current_url"))

    raise Http404("task_status_switch view error")
