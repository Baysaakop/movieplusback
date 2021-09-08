from .views import AuthorViewSet, CategoryViewSet, CommentViewSet, ArticleViewSet, ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'reviews', ReviewViewSet, basename='reviews')
urlpatterns = router.urls
