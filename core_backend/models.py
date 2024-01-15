from django.db import models
import uuid

# Define the GameModel
class GameModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)


class AnswerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gameId = models.CharField(max_length = 225)
    answer = models.CharField(max_length = 225)
    answered = models.BooleanField(default=False)

    