from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        position_admin = Position.objects.create(
            name="Back-end Developer"
        )
        position_worker = Position.objects.create(
            name="Project Manager"
        )

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testPassword123",
            position=position_admin,
        )
        self.client.force_login(self.admin_user)

        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testPassword123",
            position=position_worker,
        )

    def test_worker_position_listed(self):
        """
        Test that worker position is in list_display on worker admin page
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.position.name)

    def test_worker_detail_position_listed(self):
        """
        Test that worker's position is on worker detail admin page
        """
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.worker.position.name)

    def test_worker_detail_additional_info_listed(self):
        """
        Test that worker's Additional Info is on worker's detail admin page
        """
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)
        self.assertContains(res, "Additional info")
        self.assertContains(res, "fields")
        self.assertContains(res, self.worker.first_name)
        self.assertContains(res, self.worker.last_name)
