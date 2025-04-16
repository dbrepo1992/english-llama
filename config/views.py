from django.shortcuts import render

def homepage(request):
    return render(request, 'games/homepage.html')

def memory_game(request):
    return render(request, 'games/memory_game.html')

def leaderboard(request):
    return render(request, 'games/leaderboard.html')
