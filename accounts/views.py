from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile(request):
    user_results = GameResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'user_results': user_results
    })



def homepage(request):
    return render(request, 'games/homepage.html', {'now': now()})
