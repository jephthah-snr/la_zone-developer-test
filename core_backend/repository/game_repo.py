from core_backend.models import GameModel
from django.shortcuts import get_object_or_404



class GameRepository:
    def get_game_by_id(game_id):
        try:
            return get_object_or_404(GameModel, id=game_id)
        except GameModel.DoesNotExist:
            return None

    @staticmethod
    def update_game_by_id(game_id, data):
        game = GameModel.objects.get(id=game_id)
        for key, value in data.items():
            setattr(game, key, value)
        game.save()
        return game

    @staticmethod
    def get_all_games():
        return GameModel.objects.all()