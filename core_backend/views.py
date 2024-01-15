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

        if(game_data.is_completed == True):
            raise Exception("Game already completed, please start another game to continue playing")


        page_number = random.randrange(1, 20)

        movie_data = get_movie(page_number)
        random_user = get_random_user()

        movie_data_api_response = json.loads(movie_data)
        random_user_api_response = json.loads(random_user)

        object_count = random.randrange(len(movie_data_api_response['results']))

        api_data = movie_data_api_response['results'][object_count]
        api_data2 = movie_data_api_response['results'][random.randrange(int(object_count) + 1)]

        actor_name = api_data["name"]
        actor_name_2 = api_data2["name"]

        movie_name = api_data["known_for"][0]["original_title"]


        answer = AnswerModel.objects.create(gameId=game_id, answer=actor_name)

        actors = get_shuffled_names(actor_name, actor_name_2)

        response = {
            "answer_id": answer.id,
            "data": {
                "question": f"which of these actors starrd in the movie {movie_name}",
                "options": actors
            }
        }
        
    except Exception as e:
        response = {
            "status": False,
            "message": str(e),
        }

    return Response(response)


@api_view(["POST"])
def submit_answer(request, *args, **kwargs):
    game_id = kwargs['hash']

    body = request.body
    serialized = json.loads(body)

    quizId = serialized["quizId"]

    #validate user input
    answer_data = get_object_or_404(AnswerModel, id=quizId)
    game_data = get_object_or_404(GameModel, id=game_id)

    if(answer_data.gameId != game_id):
        raise Exception("Invalid game id provided")

    if(game_data.is_completed == True):
        raise Exception("Game already completed, please start another game to continue playing")
    
    #check answer
    user_response = serialized["answer"]

    if(user_response != answer_data.answer):
        GameModel.objects.filter(id=game_id).update(is_completed=True)

        response  = {
            "status": "false",
            "message": f"oops you got that wrong the correct answer was {user_response}"
        }

    else:
        game_data.score += 5 #decided to give 5 points for every question answered correctly
    
        GameModel.objects.filter(id=game_id).update(score=game_data.score, is_completed=False)

        response  = {
            "status": "true",
            "message": f"correct answer",
            "score": game_data.score
        }

    return Response(response)