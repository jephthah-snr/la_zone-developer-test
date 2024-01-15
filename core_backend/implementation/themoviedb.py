import requests
import os

def get_movie(page):
    print(f'page number {page}')
    url = os.getenv(f'THEMOVIE_DB_BASE_URL&page={page}', default=f'https://api.themoviedb.org/3/person/popular?language=en-US&page={page}')

    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('THEMOVIE_DB_AUTH')}"
    }

    response = requests.get(url, headers=headers)

    return response.text