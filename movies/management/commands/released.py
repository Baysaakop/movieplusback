from django.core.management.base import BaseCommand
from movies.models import Movie
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):         
        for movie in Movie.objects.all():
            movie.is_released = True           
            movie.in_theater = False
            movie.save()
        self.stdout.write(self.style.SUCCESS('Set all released'))