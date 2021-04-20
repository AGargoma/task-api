from rest_framework import serializers

from task.models import Task, TaskManager


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class TaskManagerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaskManager
        fields = ('task','upload_file','comment','score','state')
        read_only_fields = ('comment','score','state')
