from django.urls import path
from . import views

urlpatterns = [
    path('memory/', views.memory_game, name='memory_game'),
    path('submit_score/', views.submit_score, name='submit_score'),
]

