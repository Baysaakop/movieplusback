from .views import AuthorViewSet, ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'articles', ArticleViewSet, basename='articles')
urlpatterns = router.urls
