# 这将确保当Django启动时，app应用总是被导入，这样shared_task就会使用这个app应用
from .celery import app as celery_app

__all__ = ('celery_app',)