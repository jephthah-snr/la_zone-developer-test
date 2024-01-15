from django.urls import path
from . import views


urlpatterns = [
    path("/", views.start_game),
    path('/<str:hash>/play', views.play_game),
    path('/<str:hash>/play/submit', views.submit_answer, name='submit_answer'),
    path("/health", views.health_api)
]