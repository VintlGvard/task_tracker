from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{user_id}',
        {
            'type': 'notify',
            'message': message,
        }
    )

def notify_user_assignment(task):
    notify_user(task.assignee.id, f'Вы назначены ответственным за задачу: {task.title}')

def notify_status_change(task):
    notify_user(task.assignee.id, f'Статус задачи "{task.title}" изменен.')

def notify_comment_added(task):
    notify_user(task.assignee.id, f'Добавлен комментарий к задаче: {task.title}')
