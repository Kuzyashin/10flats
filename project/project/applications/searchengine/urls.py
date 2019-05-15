from .views import SearchViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'search', SearchViewSet, basename='search_view')

urlpatterns = router.urls
