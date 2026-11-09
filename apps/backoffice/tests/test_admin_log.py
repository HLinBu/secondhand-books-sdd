from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.backoffice.models import AdminLog
from apps.backoffice.services import record_admin_action


class AdminLogTests(TestCase):
    """P-05、FR-030：後台操作紀錄只能新增，不能修改或刪除。"""

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="admin@example.com", password="Test-pass-123"
        )

    def test_record_admin_action_creates_log(self):
        log = record_admin_action(self.admin, "Order #1", "裁決：賣家有理")
        self.assertEqual(AdminLog.objects.count(), 1)
        self.assertEqual(log.actor, self.admin)
        self.assertEqual(log.target, "Order #1")
        self.assertEqual(log.content, "裁決：賣家有理")
        self.assertIsNotNone(log.created_at)

    def test_existing_log_cannot_be_modified(self):
        log = record_admin_action(self.admin, "Order #1", "原內容")
        log.content = "竄改"
        with self.assertRaises(PermissionError):
            log.save()
        self.assertEqual(AdminLog.objects.get(pk=log.pk).content, "原內容")

    def test_existing_log_cannot_be_deleted(self):
        log = record_admin_action(self.admin, "Order #1", "內容")
        with self.assertRaises(PermissionError):
            log.delete()
        self.assertEqual(AdminLog.objects.count(), 1)

    def test_bulk_delete_is_blocked(self):
        record_admin_action(self.admin, "Order #1", "內容")
        with self.assertRaises(PermissionError):
            AdminLog.objects.all().delete()
        self.assertEqual(AdminLog.objects.count(), 1)
