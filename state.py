from django.db import models


class State(models.TextChoices):
    ASSIGNED = 'assigned', 'Assigned'
    COMPLETED = 'completed', 'Completed'
    ASSESSED = 'assessed', 'Assessed'


