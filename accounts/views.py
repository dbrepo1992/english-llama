from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Avg, Min, Max, Count
from games.models import GameResult
from django.utils.timezone import now

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lesson_list')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    results = GameResult.objects.filter(user=user).order_by('-created_at')

    stats = results.aggregate(
        total_games=Count('id'),
        average_score=Avg('score'),
        average_time=Avg('time'),
        first_game=Min('created_at'),
        last_game=Max('created_at'),
    )

    best_scores = {}
    for difficulty in ['easy', 'medium', 'hard']:
        best = results.filter(difficulty=difficulty).order_by('-score', 'time').first()
        if best:
            best_scores[difficulty] = best

    context = {
        'user': user,
        'user_results': results[:10],
        'best_scores': best_scores,
        'stats': stats,
    }
    return render(request, 'accounts/profile.html', context)

def homepage(request):
    return render(request, 'games/homepage.html', {'now': now()})



