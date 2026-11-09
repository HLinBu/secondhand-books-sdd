from .models import AdminLog


def record_admin_action(actor, target, content):
    """寫入一筆後台操作紀錄：操作者、時間、對象、內容（FR-030）。"""
    return AdminLog.objects.create(actor=actor, target=str(target), content=content)
