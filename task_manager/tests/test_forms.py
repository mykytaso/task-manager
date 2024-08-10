from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from task_manager.forms import TaskForm
from task_manager.models import Position, TaskType, TaskPriority


class FormsTests(TestCase):
    def test_task_creation_form(self):
        position = Position.objects.create(
            name="test_position",
        )
        get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        task_type = TaskType.objects.create(
            name="test_type"
        )
        task_priority = TaskPriority.objects.create(
            importance=1,
            name="test_task_priority",
        )
        form_data = {
            "name": "test_task_name",
            "description": "test_task_description",
            "deadline": timezone.now().date(),
            "is_completed": True,
            "priority": task_priority,
            "task_type": task_type,
            "assignees": get_user_model().objects.all(),
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertQuerysetEqual(form.cleaned_data, form_data)
