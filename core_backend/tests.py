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
import json


class HealthAPITestCase(TestCase):
    def test_health_api(self):
        url = reverse('health_api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['status'])
        self.assertIn('backend server running', response.json()['message'])


class StartGameAPITestCase(APITestCase):
    def test_start_game(self):
        url = reverse('start_game')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('game_id', response.json()['data'])
        self.assertIn('score', response.json()['data'])


class PlayGameAPITestCase(APITestCase):
    def test_play_game(self):
        game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)
        url = reverse('play_game', kwargs={'hash': game.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.json())
        self.assertIn('answer_id', response.json())
        self.assertIn('movie', response.json())
        self.assertIn('actors', response.json())

    def test_play_game_completed(self):
        game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=True)
        url = reverse('play_game', kwargs={'hash': game.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Game already completed', response.json()['message'])


class SubmitAnswerAPITestCase(APITestCase):
    def test_submit_answer_correct(self):
        game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)
        quiz = QuizModel.objects.create(id='9f8b98b0-ac76-4f1c-b01d-88d150f33dc0', game_id=game, answered=False, correct_answer='correct_answer')
        
        url = reverse('submit_answer', kwargs={'hash': game.id})
        data = {"quizId": quiz.id, "answer": "correct_answer"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.json())
        self.assertIn('message', response.json())
        self.assertIn('score', response.json()['data'])

    def test_submit_answer_wrong(self):
        game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)
        quiz = QuizModel.objects.create(id='9f8b98b0-ac76-4f1c-b01d-88d150f33dc0', game_id=game, answered=False, correct_answer='correct_answer')
        
        url = reverse('submit_answer', kwargs={'hash': game.id})
        data = {"quizId": quiz.id, "answer": "wrong_answer"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Oops! You got that wrong', response.json()['message'])

    def test_submit_answer_already_answered(self):
        game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)
        quiz = QuizModel.objects.create(id='9f8b98b0-ac76-4f1c-b01d-88d150f33dc0', game_id=game, answered=True, correct_answer='correct_answer')
        
        url = reverse('submit_answer', kwargs={'hash': game.id})
        data = {"quizId": quiz.id, "answer": "correct_answer"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Quiz has already been answered', response.json()['message'])


class GetScoreAPITestCase(APITestCase):
    def test_get_score(self):
        game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=10, is_completed=False)
        url = reverse('get_score', kwargs={'hash': game.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('game', response.json())
        self.assertIn('score', response.json())


class TestSaveActorAndMovies(unittest.TestCase):
    @patch('core_backend.implementation.external_api.get_movie')
    def test_save_actor_and_movies(self, mock_get_movie):
        # Prepare mock data for the external API response
        mock_data = {
            "results": [
                {
                    "name": "John Doe",
                    "id": 123,
                    "profile_path": "/profile.jpg",
                    "known_for": [
                        {
                            "original_title": "Movie 1",
                            "overview": "Overview 1",
                            "poster_path": "/poster1.jpg",
                            "id": 1,
                            "media_type": "movie",
                        },
                        {
                            "original_title": "Movie 2",
                            "overview": "Overview 2",
                            "poster_path": "/poster2.jpg",
                            "id": 2,
                            "media_type": "movie",
                        }
                    ]
                }
            ]
        }

        # Set up the mock response from the external API
        mock_get_movie.return_value = json.dumps(mock_data)

        # Call the function to save actors and movies
        save_actor_and_movies()

        # Assert that the external API was called
        mock_get_movie.assert_called_once_with(mock_get_movie.return_value)

        # Assert that the ActorModel and MovieModel entries were created
        actor = ActorModel.objects.get(actor_name="John Doe")
        self.assertEqual(actor.actor_id, 123)
        self.assertEqual(actor.actor_poster_url, "/profile.jpg")

        movie1 = MovieModel.objects.get(title="Movie 1")
        movie2 = MovieModel.objects.get(title="Movie 2")

        self.assertEqual(movie1.overview, "Overview 1")
        self.assertEqual(movie1.poster_path, "/poster1.jpg")
        self.assertEqual(movie1.movie_id, 1)
        self.assertEqual(movie1.media_type, "movie")

        self.assertEqual(movie2.overview, "Overview 2")
        self.assertEqual(movie2.poster_path, "/poster2.jpg")
        self.assertEqual(movie2.movie_id, 2)
        self.assertEqual(movie2.media_type, "movie")