from rest_framework import serializers
from .models import MovieModel, QuizModel

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizModel
        fields = '__all__'