from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """平台使用者（data-model：User）。

    - Email 作為登入帳號，不可重複
    - 角色：一般使用者或管理員（AI-10）；管理員可進入後台
    - is_active=False 表示停權（AI-06）
    - 密碼由 AbstractBaseUser 以雜湊保存（NFR-003）
    """

    class Role(models.TextChoices):
        MEMBER = "member", "一般使用者"
        ADMIN = "admin", "管理員"

    email = models.EmailField("Email", unique=True)
    nickname = models.CharField("暱稱", max_length=50)
    role = models.CharField("角色", max_length=10, choices=Role.choices, default=Role.MEMBER)
    email_verified = models.BooleanField("Email 已驗證", default=False)
    deletion_requested_at = models.DateTimeField("刪除帳號申請時間", null=True, blank=True)
    is_active = models.BooleanField(
        "啟用中", default=True, help_text="取消勾選即為停權，停權的使用者不能登入。"
    )
    is_staff = models.BooleanField("可進入後台", default=False, editable=False)
    date_joined = models.DateTimeField("註冊時間", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "使用者"
        verbose_name_plural = "使用者"

    def __str__(self):
        return f"{self.nickname}（{self.email}）"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def save(self, *args, **kwargs):
        # 後台權限完全由角色決定：管理員可進入後台並使用全部功能，一般使用者不行。
        self.is_staff = self.is_admin_role
        self.is_superuser = self.is_admin_role
        super().save(*args, **kwargs)
