from rest_framework import routers
from .api import KeyViewSet

router = routers.DefaultRouter()
router.register('api/keywords', KeyViewSet, 'keywords')

urlpatterns = router.urls
