from celery import shared_task
from celery.result import AsyncResult

@shared_task
def add_online_user(username, token):
    """
    将用户的用户账号和token存入redis中
    :param username: 用户账号
    :param token: token
    :return: 返回用户账号和token
    """
    return {"username": username, "token": token}

# ignore_result=True忽视该任务产生的结果并且不写入redis中
@shared_task(ignore_result=True)
def reduce_online_user(celery_task_id):
    if celery_task_id:
        # 使用 AsyncResult 获取任务结果对象，并删除 Redis 中的数据
        result = AsyncResult(celery_task_id)
        # 这将从 Redis 中删除任务结果
        result.forget()
