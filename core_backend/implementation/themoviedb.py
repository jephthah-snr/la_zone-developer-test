import requests
import os

def get_movie():
    url = os.getenv('THEMOVIE_DB_BASE_URL', default='https://api.themoviedb.org/3/person/popular?language=en-US&page=1')

    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('THEMOVIE_DB_AUTH')}"
    }

    response = requests.get(url, headers=headers)

    return response.text