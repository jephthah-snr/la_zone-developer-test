# Generated by Django 5.0.1 on 2024-01-14 01:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
    ]
