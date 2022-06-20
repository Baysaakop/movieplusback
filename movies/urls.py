from .views import GenreViewSet, RatingViewSet, ProductionViewSet, ReviewViewSet, OccupationViewSet, PlatformViewSet, CastMemberViewSet, CrewMemberViewSet
from .artistViews import ArtistViewSet
from .filmViews import MovieViewSet
from .seriesViews import SeriesViewSet
from movies.films.views import MovieListViewSet, MovieDetailViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'movielist', MovieListViewSet, basename='movielist')
router.register(r'moviedetail', MovieDetailViewSet, basename='moviedetail')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'productions', ProductionViewSet, basename='productions')
router.register(r'occupations', OccupationViewSet, basename='occupations')
# router.register(r'comments', ReviewViewSet, basename='comments')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'platforms', PlatformViewSet, basename='platforms')
router.register(r'artists', ArtistViewSet, basename='artists')
router.register(r'films', MovieViewSet, basename='films')
router.register(r'series', SeriesViewSet, basename='series')
router.register(r'castmembers', CastMemberViewSet, basename='castmembers')
router.register(r'crewmembers', CrewMemberViewSet, basename='crewmembers')
urlpatterns = router.urls
