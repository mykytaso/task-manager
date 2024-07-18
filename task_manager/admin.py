from django.contrib import admin

from task_manager.models import Position, Task, TaskType, Worker
from django.contrib.auth.admin import UserAdmin


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    )


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )
