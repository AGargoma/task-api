from django.db.models import Sum
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from question.models import QuestionManager
from quiz.models import Quiz, QuizManager
from quiz.serializers import QuizSerializer, QuizManagerSerializer
from state import State
from task.models import TaskManager


class QuizViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizManagerViewSet(viewsets.ModelViewSet):
    queryset = QuizManager.objects.all()
    serializer_class = QuizManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        self.make_assessment(serializer.instance)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def make_assessment(self, instance):
        instance.state = State.ASSESSED
        quiz_questions = instance.quiz.questions.get_queryset()
        answered_questions = QuestionManager.objects.filter(user=instance.user, question__in=quiz_questions)
        instance.score = round(answered_questions.aggregate(Sum('score'))['score__sum'] \
                               / quiz_questions.aggregate(Sum('max_score'))['max_score__sum'] * 10)

    def get_queryset(self):

        # processing of 'filter' query parameter
        try:
            filter = self.request.query_params.get('filter', None)
            filter = State(filter)
            return QuizManagerViewSet.queryset.filter(state=filter)
        except:
            return QuizManagerViewSet.queryset

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
        response = {'average_mark': round(average_mark), 'quizzes': serializer.data}
        return Response(response)
