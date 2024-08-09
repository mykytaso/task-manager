from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from task_manager.models import Task, TaskPriority, Position, TaskType


class ModelTests(TestCase):

    def test_position_str(self):
        position = Position.objects.create(
            name="test",
        )
        self.assertEqual(str(position), position.name)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(
            name="test",
        )
        self.assertEqual(str(task_type), task_type.name)

    def test_task_priority_str(self):
        task_priority = TaskPriority.objects.create(
            importance=1,
            name="test",
        )
        self.assertEqual(str(task_priority), task_priority.name)

    def test_worker_str(self):
        position = Position.objects.create(
            name="test_position",
        )
        worker = get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        self.assertEqual(
            str(worker), f"{worker.username}  ({worker.position})"
        )

    def test_worker(self):
        username = "test_worker"
        password = "test1234R"
        first_name = "test_first_name"
        last_name = "test_last_name"

        position = Position.objects.create(
            name="test_position",
        )
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.first_name, first_name)
        self.assertEqual(worker.last_name, last_name)
        self.assertEqual(worker.position, position)

    def test_task_str(self):
        task_priority = TaskPriority.objects.create(
            importance=1,
            name="test",
        )
        task_type = TaskType.objects.create(
            name="test",
        )
        position = Position.objects.create(
            name="test_position",
        )
        worker = get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        task = Task.objects.create(
            name="test",
            description="test_description",
            deadline=timezone.now().date(),
            is_completed=False,
            priority=task_priority,
            task_type=task_type,
        )

        task.assignees.set([worker])

        self.assertEqual(
            str(task),
            f"{task.name} (Type: {task.task_type}, "
            f"Priority: {task.priority}, Deadline: {task.deadline})"
        )
