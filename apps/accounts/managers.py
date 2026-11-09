from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """建立使用者。註冊一律是一般使用者；管理員只能由平台建立（AI-13）。"""

    use_in_migrations = True

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError("必須提供 Email")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields["role"] = self.model.Role.MEMBER
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["role"] = self.model.Role.ADMIN
        extra_fields.setdefault("email_verified", True)
        extra_fields.setdefault("nickname", "管理員")
        return self._create(email, password, **extra_fields)
