from rest_framework import serializers

from quiz.models import Quiz, QuizManager


class QuizSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'

class QuizManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuizManager
        fields = ('quiz','score',)
        read_only_fields = ('score',)