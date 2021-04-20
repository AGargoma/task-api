from django.db import models

from state import State


class Choice(models.Model):
    choice = models.TextField()
    question = models.ForeignKey('Question',on_delete=models.CASCADE,
                                 related_name='choices')
    is_correct = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['choice', 'question'],
                name='unique choice'
            )
        ]
    def __str__(self):
        return self.choice

class Question(models.Model):
    question = models.TextField(unique=True)
    max_score = models.IntegerField(default=1)
    published_counter = models.IntegerField(default=-1)
    # how many times question appeared as "question of the day"

    def __str__(self):
        return self.question

class QuestionManager(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    question = models.ForeignKey('Question',on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    state = models.CharField(max_length=10, choices=State.choices,
                             default=State.ASSIGNED)


class ChoiceManager(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice',on_delete=models.CASCADE)
    question = models.ForeignKey('question.Question',on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)
