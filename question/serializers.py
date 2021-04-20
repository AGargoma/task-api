from rest_framework import serializers

from question.models import Question, Choice, QuestionManager, ChoiceManager


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Choice
        fields = ('question','choice')
        extra_kwargs = {
            'write_only': 'is_correct'
        }

class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('question','max_score','choices')



class ChoiceManagerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ChoiceManager
        fields = ('question', 'choice' )

class QuestionManagerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = QuestionManager
        fields = ('question','score')
        read_only_fields = ('score',)
