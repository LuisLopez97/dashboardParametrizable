from rest_framework import routers
from .api import KeyViewSet

# Creacion de ruta para el backend.
router = routers.DefaultRouter()
router.register('api/keywords', KeyViewSet, 'keywords')

urlpatterns = router.urls
