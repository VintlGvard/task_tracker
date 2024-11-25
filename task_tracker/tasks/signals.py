from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Comment
from .tasks import notify_user_assignment, notify_status_change, notify_comment_added

@receiver(post_save, sender=Task)
def task_saved(sender, instance, created, **kwargs):
    if created:
        notify_user_assignment(instance)
    else:
        notify_status_change(instance)

@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created, **kwargs):
    if created:
        notify_comment_added(instance.task)
