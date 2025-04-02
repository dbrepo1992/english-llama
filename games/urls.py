from django.urls import path
from . import views

urlpatterns = [
    path('memory/', views.memory_game, name='memory_game'),
]
