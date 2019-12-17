from rest_framework import routers
from .api import BusquedaViewSet

router = routers.DefaultRouter()
router.register('db/busquedas', BusquedaViewSet, 'busquedas')

urlpatterns = router.urls
