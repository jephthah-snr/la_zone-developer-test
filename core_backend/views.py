from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core_backend.repository.quiz_repo import get_quiz_by_id, update_quiz_by_id
from core_backend.repository.game_repo import get_game_by_id, update_game_by_id
from . models import GameModel, QuizModel, MovieModel, ActorModel
from django.shortcuts import get_object_or_404
from lazone_api_service.utils import get_shuffled_names
from lazone_api_service.shared.app_error import CustomError
from core_backend.helpers.fetchMovieHelper import save_actor_and_movies
from core_backend.helpers.response import success_response, error_response
from rest_framework import status
from core_backend.serializers import QuizSerializer




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
                'status': True,
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
        game_id = kwargs.get('hash')
        quiz_id = request.data.get("quizId")
        answer = request.data.get("answer")

        quiz = get_quiz_by_id(quiz_id)
        game = get_game_by_id(game_id)

        if quiz.answered:
            return error_response('Quiz has already been answered, move on to the next one', status.HTTP_400_BAD_REQUEST)


        if str(quiz.game_id) != game_id:
            return error_response('Invalid game id provided', status.HTTP_400_BAD_REQUEST)

        if game.is_completed:
            return error_response('Game already completed, please start another game to continue playing', status.HTTP_400_BAD_REQUEST)

        if answer == quiz.correct_answer:
            score = game.score + 5
            update_game_by_id(game_id, {'score': score})
            update_quiz_by_id(quiz_id, {'answered': True})
            return success_response('Answer submitted successfully', status.HTTP_200_OK, {'score': score})
        else:
            update_game_by_id(game_id, {'is_completed': True})
            return error_response(f'Oops! You got that wrong.', status.HTTP_500_INTERNAL_SERVER_ERROR)
    except CustomError as error:
        return Response({"error": str(error)}, status=error.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_score(request, *args, **kwargs):
    try:
        game_id = kwargs['hash']

        game_data = get_game_by_id(game_id)

        score = game_data.score

        response = {
            'game': game_id,
            'score': score
        }
        return success_response('Answer submitted successfully', status.HTTP_200_OK, response)
    except CustomError as error:
        return Response({"error": str(error)}, status=error.status_code)