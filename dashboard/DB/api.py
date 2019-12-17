from DB.models import Busquedas
from rest_framework import viewsets, permissions
from .serializer import BusquedaSerializer

# Busquedas Viewset


class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busquedas.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = BusquedaSerializer
