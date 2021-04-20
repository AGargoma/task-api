from django.db import models

from state import State


class Quiz(models.Model):
    title = models.CharField(max_length=100,default='Quiz')
    questions = models.ManyToManyField('question.Question')
    deadline = models.DateTimeField()


class QuizManager(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz',on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    state = models.CharField(max_length=10,choices=State.choices,
                             default=State.ASSIGNED)
    correct_answer_count = models.IntegerField(default=0,editable=False)

