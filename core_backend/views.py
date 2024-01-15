from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.forms import model_to_dict
from rest_framework.response import Response
from core_backend.repository import game_repo
from . models import GameModel
from django.shortcuts import get_object_or_404
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
    try:
        hash_value = kwargs['hash']
      
        data = get_object_or_404(GameModel, id=hash_value)

        response = model_to_dict(data)

        if(not response):
            raise Exception("Invalid Hash")
        
    except KeyError:
        response = {
            "status": False,
            "message": "Hash parameter is missing.",
        }

    return Response(response)