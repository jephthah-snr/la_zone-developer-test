from django.urls import path
from . import views


urlpatterns = [
    path('', views.start_game, name='start_game'),
    path('/<str:hash>/play', views.play_game, name='play_game'),
    path('/<str:hash>/play/submit', views.submit_answer, name='submit_answer'),
    path('/<str:hash>', views.get_score, name='submit_answer'),
    path('/health/readyz', views.health_api)
]