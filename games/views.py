from django.shortcuts import render

def memory_game(request):
    return render(request, 'games/memory_game.html')
