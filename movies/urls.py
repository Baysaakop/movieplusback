from .views import GenreViewSet, RatingViewSet, ProductionViewSet, CommentViewSet, OccupationViewSet, CastMemberViewSet, CrewMemberViewSet
from .artistViews import ArtistViewSet
from .filmViews import MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'productions', ProductionViewSet, basename='productions')
router.register(r'occupations', OccupationViewSet, basename='occupations')
router.register(r'comments', CommentViewSet, basename='comments')
# router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'artists', ArtistViewSet, basename='artists')
router.register(r'films', MovieViewSet, basename='films')
router.register(r'castmembers', CastMemberViewSet, basename='castmembers')
router.register(r'crewmembers', CrewMemberViewSet, basename='crewmembers')
# router.register(r'series', SeriesViewSet, basename='series')
urlpatterns = router.urls
