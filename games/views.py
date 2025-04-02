from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameResult
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
def submit_score(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        time = data.get('time')
        score = data.get('score')

        result = GameResult.objects.create(
            user=request.user,
            time=time,
            score=score
        )
        return JsonResponse({'status': 'ok', 'result_id': result.id})
    return JsonResponse({'status': 'unauthorized'}, status=401)

@login_required
def memory_game(request):
    return render(request, 'games/memory_game.html')
