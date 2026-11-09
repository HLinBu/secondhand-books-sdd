from django.conf import settings
from django.db import models


class AdminLogQuerySet(models.QuerySet):
    """禁止批次修改與刪除，確保紀錄只能新增。"""

    def update(self, **kwargs):
        raise PermissionError("後台操作紀錄不能修改。")

    def delete(self):
        raise PermissionError("後台操作紀錄不能刪除。")


class AdminLog(models.Model):
    """後台操作紀錄（data-model：P-05、FR-030）。紀錄只能新增，不能修改或刪除。"""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="操作者",
        on_delete=models.PROTECT,
        related_name="admin_logs",
    )
    created_at = models.DateTimeField("時間", auto_now_add=True)
    target = models.CharField("對象", max_length=200)
    content = models.TextField("內容")

    objects = AdminLogQuerySet.as_manager()

    class Meta:
        verbose_name = "後台操作紀錄"
        verbose_name_plural = "後台操作紀錄"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.target}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise PermissionError("後台操作紀錄不能修改。")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionError("後台操作紀錄不能刪除。")
