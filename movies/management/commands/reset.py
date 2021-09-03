from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for movie in Movie.objects.all():
            movie.view_count = 0
            movie.like_count = 0
            movie.watched_count = 0
            movie.watchlist_count = 0
            movie.score_count = 0
            movie.avg_score = 0
            movie.save()
        # for artist in Artist.objects.all():
        #     artist.views = 0
        #     artist.likes = 0
        #     artist.followers = 0
        #     artist.save()
        # for review in Review.objects.all():
        #     review.views = 0
        #     review.likes = 0
        #     review.score = 0
        #     review.save()
        self.stdout.write(self.style.SUCCESS('Reset all data'))
