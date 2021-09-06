from django.contrib import admin
from .models import Genre, Rating, Production, Occupation, Artist, Comment, Movie, CastMember, CrewMember

admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Production)
admin.site.register(Occupation)
admin.site.register(Artist)
admin.site.register(Comment)
admin.site.register(Movie)
admin.site.register(CastMember)
admin.site.register(CrewMember)
