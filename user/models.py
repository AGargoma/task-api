from django.db import models
from django.contrib.auth.models import AbstractUser as UserModel


class User(UserModel):
    questions = models.ManyToManyField('question.Question',
                                       through='question.QuestionManager')
    choices = models.ManyToManyField('question.Choice',through='question.ChoiceManager')
    quizzes = models.ManyToManyField('quiz.Quiz', through='quiz.QuizManager')
    tasks = models.ManyToManyField('task.Task', through='task.TaskManager')
    username = models.CharField(max_length=30, unique=True)






