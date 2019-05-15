from .views import SearchViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r'search', SearchViewSet, basename='search_view')

urlpatterns = router.urls
