import os

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from quiz.models import QuizManager
from state import State
from task.models import Task, TaskManager
from task.serializers import TaskSerializer, TaskManagerSerializer


class TaskViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskManagerViewSet(viewsets.ModelViewSet):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        serializer.instance.state = State.COMPLETED
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):

        # processing of 'filter' query parameter
        try:
            filter = self.request.query_params.get('filter', None)
            filter = State(filter)
            return TaskManagerViewSet.queryset.filter(state=filter)
        except:
            return TaskManagerViewSet.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        total_quiz_mark = QuizManager.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum']
        total_task_mark = TaskManager.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum']
        if total_quiz_mark is None:
            total_quiz_mark = 0
        if total_task_mark is None:
            total_task_mark = 0
        try:
            average_mark = (total_quiz_mark + total_task_mark) \
                           / (QuizManager.objects.filter(user=request.user).count()
                              + TaskManager.objects.filter(user=request.user).count())
        except ZeroDivisionError:
            average_mark = 0

        response = {'average_mark': round(average_mark), 'tasks': serializer.data}
        return Response(response)


def download(request, *args, **kwargs):
    file_path = os.path.join(settings.MEDIA_ROOT, request.path[1:])
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise status.HTTP_404_NOT_FOUND
