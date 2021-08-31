from .views import ItemViewSet, PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')
router.register(r'posts', PostViewSet, basename='posts')
urlpatterns = router.urls

# from django.urls import path
# from .views import ItemListView, ItemDetailView, ItemCreateView, ItemUpdateeView, ItemDetailView

# urlpatterns = [
#     path('', ItemListView.as_view()),    
#     path('<pk>', ItemDetailView.as_view()),    
# ]