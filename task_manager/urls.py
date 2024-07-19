from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
    TaskListView,
    TaskTypeListView,
    PositionListView,
    WorkerDetailView,
    TaskDetailView,
    PositionCreateView,
    PositionDeleteView,
    PositionUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task_types/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),

]

app_name = "task_manager"
