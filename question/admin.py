from django.contrib import admin

from question.models import Question, Choice, QuestionManager, ChoiceManager

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionManager)
admin.site.register(ChoiceManager)

