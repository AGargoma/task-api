from django.contrib import admin

from quiz.models import Quiz, QuizManager

admin.site.register(Quiz)
admin.site.register(QuizManager)
