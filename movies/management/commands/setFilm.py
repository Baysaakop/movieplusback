from django.core.management.base import BaseCommand
from movies.models import Movie, Film

class Command(BaseCommand):
    def handle(self, *args, **kwargs):         
        for movie in Movie.objects.all():
            Film.objects.create(movie=movie)
        self.stdout.write(self.style.SUCCESS('Set Film'))