from .views import GenreViewSet, RatingViewSet, ProductionViewSet, OccupationViewSet, CastMemberViewSet, CrewMemberViewSet
from .artistViews import ArtistViewSet
from .filmViews import MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'productions', ProductionViewSet, basename='productions')
router.register(r'occupations', OccupationViewSet, basename='occupations')
# router.register(r'scores', ScoreViewSet, basename='scores')
# router.register(r'comments', CommentViewSet, basename='comments')
# router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'artists', ArtistViewSet, basename='artists')
# router.register(r'tempartists', TempArtistViewSet, basename='tempartists')
# router.register(r'members', MemberViewSet, basename='members')
# router.register(r'actors', ActorViewSet, basename='actors')
# router.register(r'tempmembers', TempMemberViewSet, basename='tempmembers')
# router.register(r'tempactors', TempActorViewSet, basename='tempactors')
router.register(r'films', MovieViewSet, basename='films')
router.register(r'castmembers', CastMemberViewSet, basename='castmembers')
router.register(r'crewmembers', CrewMemberViewSet, basename='crewmembers')
# router.register(r'films', FilmViewSet, basename='films')
# router.register(r'tempfilms', TempFilmViewSet, basename='tempfilms')
# router.register(r'series', SeriesViewSet, basename='series')
urlpatterns = router.urls
