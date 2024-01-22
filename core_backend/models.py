from django.db import models
import uuid

# Define the GameModel
class GameModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    played_quizzes = models.ManyToManyField('QuizModel')
    score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Game {self.id}"
    

class QuizModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_id = models.CharField(max_length=255)
    movie_id = models.CharField(max_length=255)
    actor_id1 = models.CharField(max_length=255)
    actor_id2 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Quiz {self.id}"

class AnswerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gameId = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    answer = models.CharField(max_length=225)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer {self.id}"
    

class ActorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_id = models.IntegerField(unique=True) 
    actor_name = models.CharField(max_length=255)
    actor_poster_url = models.URLField()

    def __str__(self):
        return self.actor_name

class MovieModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    overview =  models.TextField()
    poster_path = models.CharField(max_length=255)
    actor = models.ForeignKey(ActorModel, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

