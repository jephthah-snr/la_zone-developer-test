import requests

def get_movie():
    url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=1"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYTIzYzFkODMxMTFiZmM0ZjE3YTkxYTI4YmY2MGI4YiIsInN1YiI6IjY1YTJlMWQ5YTZhNGMxMDEzMWE0NzhlOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jXjzoyeIEmFlN6JBFkLloT9QFxT2msE-cgoX42A1If8"
    }

    response = requests.get(url, headers=headers)

    return response.text