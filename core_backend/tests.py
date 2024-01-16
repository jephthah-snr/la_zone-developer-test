from django.test import TestCase
from django.urls import reverse
from core_backend.models import GameModel, AnswerModel
from rest_framework import status
from rest_framework.test import APIRequestFactory
from . views import submit_answer, play_game, start_game

factory = APIRequestFactory()

class AnswerQuizTestCase(TestCase):
    def setUp(self):
        self.game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)
        self.answer = AnswerModel.objects.create(id='9f8b98b0-ac76-4f1c-b01d-88d150f33dc0', gameId=self.game, answer='correct_answer', answered=False)


    def test_submit_correct_answer(self):
        game_id = 'f6d844d5-88a9-4b44-b328-661069aeeec9'
        quiz_id = '9f8b98b0-ac76-4f1c-b01d-88d150f33dc0'

        payload = {
            "quizId": quiz_id,
            "answer": "correct_answer",
        }

        url = reverse('submit_answer', kwargs={'hash': game_id})

        request = factory.post(url, payload, format='json')
        response = submit_answer(request, hash=game_id)
        self.assertEqual(response.data['status'], True)
        self.assertEqual(response.data['message'], 'Correct answer')

        status_code = response.status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

        self.game.refresh_from_db()
        self.answer.refresh_from_db()

        self.assertEqual(self.game.score, 5)
        self.assertTrue(self.answer.answered)
        self.assertFalse(self.game.is_completed)


class PlayGameTestCase(TestCase):
    def setUp(self):
        self.game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)

    def test_completed_game(self):
        game_id = 'f6d844d5-88a9-4b44-b328-661069aeeec9'

        url = reverse('play_game', kwargs={'hash': game_id})

        request = factory.get(url)

        response = play_game(request, hash=game_id)

        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response(self):
        game_id = 'f6d844d5-88a9-4b44-b328-661069aeeec9'

        url = reverse('play_game', kwargs={'hash': game_id})

        request = factory.get(url)

        response = play_game(request, hash=game_id)

        quiz_data = response.data.get('data', {})
        question = quiz_data.get('question', '')
        options = quiz_data.get('options', [])

        self.assertEqual(question,  question)
        self.assertIsInstance(question, str)
        self.assertIsInstance(options, list)


class StartGameTestCase(TestCase):
    def setUp(self):
        self.game = GameModel.objects.create(id='f6d844d5-88a9-4b44-b328-661069aeeec9', score=0, is_completed=False)

    def test_startgame_response(self):
        url = reverse('start_game')

        request = factory.get(url)

        response = start_game(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertIn('id', response.data)