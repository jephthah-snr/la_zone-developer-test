from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from core_backend.models import GameModel, QuizModel, MovieModel, ActorModel
from rest_framework import status
from .views import start_game, play_game, submit_answer, get_score
from unittest.mock import patch
from core_backend.implementation.external_api import get_movie
from core_backend.models import ActorModel, MovieModel
from core_backend.helpers.fetchMovieHelper import save_actor_and_movies
from rest_framework.test import APIRequestFactory
from core_backend.views import start_game

factory = APIRequestFactory()

class HealthAPITestCase(TestCase):
    def test_health_api(self):
        url = reverse('health_api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['status'])
        self.assertIn('backend server running', response.json()['message'])
