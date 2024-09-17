import os

from celery import Celery

# 为celery程序设在默认的Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShopBackend.settings')

app = Celery('ShopBackend')

# 在这里使用字符串意味着工作进程不需要将配置对象序列化到子进程
# - namespace='CELERY'意味着所有与celery-related的配置键都应该有一个CELERY_前缀
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现每个已安装应用中的 tasks.py 文件
# 从所有已注册的Django应用中加载任务模块
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')