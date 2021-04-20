from django.contrib import admin

from task.models import Task, TaskManager

admin.site.register(Task)
admin.site.register(TaskManager)
