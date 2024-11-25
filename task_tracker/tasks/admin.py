from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'assignee')

admin.site.register(Task, TaskAdmin)