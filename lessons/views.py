from django.shortcuts import render

# Create your views here.
from .models import Lesson

def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons/lesson_list.html', {'lessons': lessons})
