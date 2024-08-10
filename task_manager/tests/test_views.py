from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Task, TaskPriority, TaskType

TASK_LIST_URL = reverse("task_manager:task-list")
TASK_DETAIL_URL = reverse("task_manager:task-detail", kwargs={"pk": 1})
WORKER_LIST_URL = reverse("task_manager:worker-list")
WORKER_DETAIL_URL = reverse("task_manager:worker-detail", kwargs={"pk": 1})
TASKTYPE_LIST_URL = reverse("task_manager:tasktype-list")
POSITION_LIST_URL = reverse("task_manager:position-list")


class PublicWorkerTest(TestCase):
    def test_login_required_worker_list_view(self):
        response = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_worker_detail_view(self):
        res = self.client.get(TASK_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(
            name="test_position",
        )
        self.worker = get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_worker_list(self):
        position_01 = Position.objects.create(
            name="test_position_01",
        )
        position_02 = Position.objects.create(
            name="test_position_02",
        )

        get_user_model().objects.create(
            username="test_worker_01",
            password="<PASSWORD>_01",
            first_name="test_first_name_01",
            last_name="test_last_name_01",
            position=position_01,
        )

        get_user_model().objects.create(
            username="test_worker_02",
            password="<PASSWORD>_02",
            first_name="test_first_name_02",
            last_name="test_last_name_02",
            position=position_02,
        )

        response = self.client.get(WORKER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        workers = get_user_model().objects.all()
        self.assertQuerysetEqual(
            response.context["worker_list"],
            workers,
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")


class PublicTaskTest(TestCase):
    def test_login_required_task_list_view(self):
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_detail_view(self):
        res = self.client.get(TASK_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(
            name="test_position",
        )
        self.worker = get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_task_list(self):
        task_priority = TaskPriority.objects.create(
            importance=1,
            name="test_task_priority",
        )
        task_type = TaskType.objects.create(
            name="test_task_type",
        )
        Task.objects.create(
            name="test_task_name_01",
            description="test_description_02",
            deadline=timezone.now().date(),
            is_completed=False,
            priority=task_priority,
            task_type=task_type,
        )
        Task.objects.create(
            name="test_task_name_92",
            description="test_description_02",
            deadline=timezone.now().date(),
            is_completed=True,
            priority=task_priority,
            task_type=task_type,
        )
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertQuerysetEqual(
            response.context["task_list"],
            tasks,
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")


class PublicTaskTypeTest(TestCase):
    def test_login_required_tasktype_list_view(self):
        response = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(
            name="test_position",
        )
        self.worker = get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_tasktype_list(self):
        TaskType.objects.create(
            name="test_task_type_01",
        )
        TaskType.objects.create(
            name="test_task_type_02",
        )
        response = self.client.get(TASKTYPE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        tasktyepes = TaskType.objects.all()
        self.assertQuerysetEqual(
            response.context["tasktype_list"],
            tasktyepes,
        )
        self.assertTemplateUsed(response, "task_manager/tasktype_list.html")


class PublicPositionTest(TestCase):
    def test_login_required_position_list_view(self):
        response = self.client.get(POSITION_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(
            name="test_position",
        )
        self.worker = get_user_model().objects.create(
            username="test_worker",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
            position=position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_position_list(self):
        Position.objects.create(
            name="test_position_01",
        )
        Position.objects.create(
            name="test_position_02",
        )
        response = self.client.get(POSITION_LIST_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertQuerysetEqual(
            response.context["position_list"],
            positions,
        )
        self.assertTemplateUsed(response, "task_manager/position_list.html")
