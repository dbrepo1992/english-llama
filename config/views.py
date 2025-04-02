from django.shortcuts import render

def homepage(request):
    return render(request, 'games/homepage.html')

