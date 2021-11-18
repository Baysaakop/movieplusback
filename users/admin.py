from django.contrib import admin
from .models import Profile, FilmDate, FilmScore, SeriesScore

admin.site.register(Profile)
admin.site.register(FilmDate)
admin.site.register(FilmScore)
admin.site.register(SeriesScore)
