from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
    TaskListView,
    TaskTypeListView,
    PositionListView,
    WorkerDetailView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionCreateView,
    PositionDeleteView,
    PositionUpdateView,
    assign_unassign_worker,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
    path("task_types/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("task_types/create/", TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("task_types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="tasktype-update"),
    path("task_types/<int:pk>/delete", TaskTypeDeleteView.as_view(), name="tasktype-delete"),

    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("tasks/assign_unassign_worker/", assign_unassign_worker, name="assign_unassign_worker"),
]

app_name = "task_manager"
