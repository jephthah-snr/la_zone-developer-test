from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.forms import model_to_dict
from rest_framework.response import Response
from core_backend.repository import game_repo
from . models import GameModel, AnswerModel
from django.shortcuts import get_object_or_404
from lazone_api_service.utils import get_shuffled_names
from core_backend.implementation.external_api import get_movie, get_random_user
from lazone_api_service.shared.app_error import CustomSuccessResponse, CustomErrorResponse, CustomError
from django.db.models import F
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

@api_view(['GET'])
def start_game(request):
    new_game = GameModel.objects.create(score=0, is_completed=False)
    new_game_id = new_game.id
    return Response({'id': new_game_id})


@api_view(["GET"])
def play_game(request, *args, **kwargs):
    api_data = {} # i added this to ensure it exists regardless of whether the try block is executed successfully
    try:
        game_id = kwargs['hash']

        game_data = get_object_or_404(GameModel, id=game_id)
        

        if game_data.is_completed:
            response = Response({"status_code": 400, "message": "Game already completed, please start another game to continue playing"})
            return response

        page_number = random.randrange(1, 20)

        movie_data = get_movie(page_number)

        movie_data_api_response = json.loads(movie_data)

        object_count = random.randrange(len(movie_data_api_response['results']))

        api_data = movie_data_api_response['results'][object_count]
        api_data2 = movie_data_api_response['results'][random.randrange(int(object_count) + 6)]

        actor_name = api_data["name"]
        actor_name_2 = api_data2["name"]

        movie_name = api_data["known_for"][0]['original_title']

        answer = AnswerModel.objects.create(gameId=game_data, answer=actor_name)


        actors = get_shuffled_names(actor_name, actor_name_2)

        response = {
            "quiz_id": answer.id,
            "data": {
                "question": f"which of these actors starred in the movie {movie_name}",
                "options": actors
            }
        }
        
        return Response(response)

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


