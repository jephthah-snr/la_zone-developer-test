from django.db import models
import uuid

# Define the GameModel
class GameModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
