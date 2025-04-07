from django.urls import path
from . import views

urlpatterns = [
    path('memory/', views.memory_game, name='memory_game'),
    path('memory/save/', views.save_result, name='save_memory_result'),
    path('submit_score/', views.submit_score, name='submit_score'),
    path('leaderboard/<str:difficulty>/', views.leaderboard, name='leaderboard'),
]

