from django.db import models
from rest_framework.exceptions import ValidationError

from state import State


class Task(models.Model):
    task = models.TextField(default=0)
    title = models.CharField(max_length=100)
    max_score = models.IntegerField(default=10)
    deadline = models.DateTimeField()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user/<filename>
    return f'download/{instance.user}/{filename}'


def validate_file_size(value):
    filesize = value.size
    if filesize > 2097152:
        raise ValidationError("The maximum file size that can be uploaded is 2MB")
    else:
        return value

class TaskManager(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    task = models.ForeignKey('Task',on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to=user_directory_path,validators=[validate_file_size])
    upload_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    state = models.CharField(max_length=10,choices=State.choices,
                             default=State.ASSIGNED)
    comment = models.TextField(default='')


