# Generated by Django 5.0.1 on 2024-01-22 15:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActorModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('actor_id', models.IntegerField(unique=True)),
                ('actor_name', models.CharField(max_length=255)),
                ('actor_poster_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='GameModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuizModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('game_id', models.CharField(max_length=255)),
                ('movie_id', models.CharField(max_length=255)),
                ('actor_id1', models.CharField(max_length=255)),
                ('actor_id2', models.CharField(max_length=255)),
                ('correct_answer', models.CharField(max_length=255)),
                ('answered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=225)),
                ('answered', models.BooleanField(default=False)),
                ('gameId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_backend.gamemodel')),
            ],
        ),
        migrations.CreateModel(
            name='MovieModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('movie_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('poster_path', models.CharField(max_length=255)),
                ('media_type', models.CharField(max_length=255)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_backend.actormodel')),
            ],
        ),
        migrations.AddField(
            model_name='gamemodel',
            name='played_quizzes',
            field=models.ManyToManyField(to='core_backend.quizmodel'),
        ),
    ]
