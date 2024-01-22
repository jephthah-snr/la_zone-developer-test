from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.forms import model_to_dict
from rest_framework.response import Response
from core_backend.repository import game_repo
from . models import GameModel, AnswerModel, QuizModel, MovieModel, ActorModel
from django.shortcuts import get_object_or_404
from lazone_api_service.utils import get_shuffled_names
from core_backend.implementation.external_api import get_movie, get_random_user
from lazone_api_service.shared.app_error import CustomSuccessResponse, CustomErrorResponse, CustomError
from core_backend.repository.game_repo import GameRepository
from core_backend.helpers.fetchMovieHelper import save_actor_and_movies
from rest_framework import status
from core_backend.serializers import QuizSerializer
from django.core.serializers import serialize
import json
import random


# Create your views here.

def health_api(request, *args, **kwargs):
    response = {
        "status": True,
        "message": "backend server running 🚀🚀🚀⚡️"
    }
    return JsonResponse(response)

@api_view(['POST'])
def start_game(request):
    try:
        new_game = GameModel.objects.create(score=0, is_completed=False)

        new_game_id = new_game.id

        for _ in range(8):
            random_movie = MovieModel.objects.order_by('?').first()

            random_actor = ActorModel.objects.exclude(id=random_movie.actor.id).order_by('?').first()

            QuizModel.objects.create(
                game_id=new_game_id,
                movie_id=random_movie.id,
                actor_id1 = random_movie.actor.id,
                actor_id2=random_actor.id,
                correct_answer = random_movie.actor.id
            )

        response = {
            'status': True,
            'message': "Game started successfully",
            'data': {
                'game_id': new_game_id,
                'score': new_game.score
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)
    except CustomError as error:
        return Response({"error": str(error)}, status=error.status_code)
        

@api_view(["GET"])
def play_game(request, *args, **kwargs):
    try:
        game_id = kwargs['hash']
        game_data = get_object_or_404(GameModel, id=game_id)

        if game_data.is_completed:
            response_data = {"message": "Game already completed, please start another game to continue playing"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        quiz = QuizModel.objects.filter(game_id=game_id, answered=False).first()

        if quiz:
            quiz_data = QuizSerializer(quiz).data

            actor1 = get_object_or_404(ActorModel, id=quiz_data.get('actor_id1'))
            actor2 = get_object_or_404(ActorModel, id=quiz_data.get('actor_id2'))
            movie =  get_object_or_404(MovieModel, id=quiz_data.get('movie_id'))

            actors = get_shuffled_names({
                       'actor_id': actor1.id,
                       'actor_name': actor1.actor_name,
                       'actor_poster_url':  actor1.actor_poster_url,
                    },
                    {
                       'actor_id': actor2.id,
                       'actor_name': actor2.actor_name,
                       'actor_poster_url':  actor2.actor_poster_url,
                    })

            response = {
                'answer_id': quiz_data.get('id'),
                'movie': {
                    'movie_id': movie.id,
                    'name': movie.title,
                    'overview': movie.overview,
                    'poster_path': movie.poster_path,
                    'media_type': movie.media_type,
                },
                'actors': actors
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response_data = {"message": "No unanswered quizzes found"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    except CustomError as error:
        return Response({"error": str(error)}, status=error.status_code)


@api_view(["POST"])
def submit_answer(request, *args, **kwargs):
    try:
        game_id = kwargs['hash']

        body = request.body
        serialized = json.loads(body)

        quiz_id = serialized.get("quizId")

        answer_data = get_object_or_404(AnswerModel, id=quiz_id)
        game_data = get_object_or_404(GameModel, id=game_id)

        serialized_gameId = AnswerModel.objects.filter(id=quiz_id).values_list('gameId', flat=True).first()

        if answer_data.answered:
            response = Response({"status_code": 400, "message": "Already answered quiz, please move to the next"})
            return response

        if str(serialized_gameId) != game_id:
            response = Response({"status_code": 400, "message": "Invalid game id provided"})
            return response

        if game_data.is_completed:
            response = Response({"status_code": 400, "message": "Game already completed, please start another game to continue playing"})
            return response

        user_response = serialized.get("answer")

        if user_response != answer_data.answer:
            GameModel.objects.filter(id=game_id).update(is_completed=True)
            response = Response({"status_code": 400, "message": f"Oops! You got that wrong. The correct answer was {answer_data.answer}"})
            return response

        else:
            game_data.score += 5  # i decided to give 5 points for every question answered correctly

            GameModel.objects.filter(id=game_id).update(score=game_data.score, is_completed=False)
            AnswerModel.objects.filter(id=quiz_id).update(answered=True)

            response = {
            "status": True,
            "message": "Correct answer",
            "score": game_data.score
            }

        return Response(response)

    except CustomError as error:
        return Response({"error": str(error)}, status=error.status_code)


@api_view(["GET"])
def get_score(request, *args, **kwargs):
    try:
        game_id = kwargs['hash']

        game_data = GameRepository.get_game_by_id(game_id)

        score = game_data.score

        print(score)

        return Response({"status_code": status.HTTP_200_OK, "message": f"you scored {score} points"})
    except CustomError as error:
        return Response({"error": str(error)}, status=error.status_code)