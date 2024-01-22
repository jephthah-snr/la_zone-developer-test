from core_backend.models import GameModel
from django.shortcuts import get_object_or_404



def get_game_by_id(game_id):
    quiz = get_object_or_404(GameModel, id=game_id)
    return quiz


def update_game_by_id(game_id, data):
    try:
        instance = GameModel.objects.get(id=game_id)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return True, instance
    except GameModel.DoesNotExist:
        return False, None