from core_backend.models import ActorModel, MovieModel
from core_backend.implementation.external_api import get_movie
import json
import random

def save_actor_and_movies():
    data = json.loads(get_movie(random.randrange(1, 12)))
    results = data.get('results')

    for entry in results:
        actor_name = entry.get('name')
        actor_id = entry.get('id')
        actor_poster_url = entry.get('profile_path')
        movies = entry.get('known_for')

        actor, created = ActorModel.objects.get_or_create(actor_name=actor_name,
        actor_id=actor_id, 
        actor_poster_url=actor_poster_url)

        actor_id = actor.id
        #print(f"Actor: {actor_name}, ID: {actor_id}")

        for item in movies:
            title = item.get('original_title') or item.get('original_name')
            overview = item.get('overview')
            poster_path = item.get('poster_path')
            movie_id = item.get('id')
            media_type = item.get('media_type')

            movie = MovieModel.objects.create(
                title = title,
                overview = overview,
                poster_path = poster_path,
                movie_id = movie_id,
                media_type = media_type,
                actor_id = actor_id
            )
            #print(f"  - Movie: {title}, ID: {movie.id}")
