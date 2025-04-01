from django.db import models

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField()

    def __str__(self):
        return self.title
