from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.forms import model_to_dict
from rest_framework.response import Response
from core_backend.repository import game_repo
from . models import GameModel, AnswerModel
from django.shortcuts import get_object_or_404
from core_backend.implementation import themoviedb
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


@api_view(['GET'])
def play_game(request, *args, **kwargs):
    api_data = {} # i added this to ensure it exists regardless of whether the try block is executed successfully
    try:
        game_id = kwargs['hash']

        game_data = get_object_or_404(GameModel, id=game_id)

        if(game_data.is_completed == True):
            raise Exception("Game already completed, please start another game to continue playing")

        print(game_data)

        page_number = random.randrange(1, 9)

        movie_data = themoviedb.get_movie(page_number)

        api_response = json.loads(movie_data)

        object_count = random.randrange(len(api_response['results']))

        api_data = api_response['results'][object_count]

        actor_name = api_data["original_name"]

        movie_name = api_data["known_for"][1]["original_title"]

        print(actor_name, movie_name)

        answerId = AnswerModel.objects.create(gameId=game_id, answer=actor_name)

        response = {
            "answer_id": answerId,
            "data": {
                "question": f"which of these actors starrd in the movie {movie_name}",
                "options": [actor_name, "John Doe"]
            }
        }
        
    except KeyError:
        response = {
            "status": False,
            "message": "Hash parameter is missing.",
        }
    except Exception as e:
        response = {
            "status": False,
            "message": str(e),
        }

    return Response(response)