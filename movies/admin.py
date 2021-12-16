from django.contrib import admin
from .models import Genre, Tag, Rating, Production, Occupation, Artist, Review, Theater, TheaterUrl, Platform, PlatformUrl, Movie, Series, CastMember, CrewMember

admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Production)
admin.site.register(Occupation)
admin.site.register(Artist)
admin.site.register(Review)
admin.site.register(Theater)
admin.site.register(TheaterUrl)
admin.site.register(Platform)
admin.site.register(PlatformUrl)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(CastMember)
admin.site.register(CrewMember)
