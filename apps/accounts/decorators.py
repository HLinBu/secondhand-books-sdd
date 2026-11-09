from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def verified_required(view_func):
    """需要登入且 Email 已驗證（AI-01：未驗證的帳號不能上架或下單）。"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not user.email_verified:
            messages.error(request, "請先完成 Email 驗證，才能上架或下單。")
            return redirect("/")
        return view_func(request, *args, **kwargs)

    return wrapper
