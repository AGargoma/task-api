from rest_framework import permissions, viewsets, mixins, status
from rest_framework.response import Response

from question.models import Question, Choice, QuestionManager, ChoiceManager
from question.serializers import QuestionSerializer, ChoiceSerializer, QuestionManagerSerializer, \
    ChoiceManagerSerializer
from state import State


class QuestionViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChoiceViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionManagerViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = QuestionManager.objects.all()
    serializer_class = QuestionManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
        selected = list(ChoiceManager.objects.filter(question=instance.question,
                                                user=instance.user,
                                                is_selected=True)\
                                                .values_list('choice',flat=True))
        correct = list(Choice.objects.filter(question=instance.question,
                                            is_correct=True).values_list('id',flat=True))
        if set(selected) == set(correct):
            instance.score = instance.question.max_score
        else:
            instance.score = 0

class ChoiceManagerViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = ChoiceManager.objects.all()
    serializer_class = ChoiceManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,is_selected=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





