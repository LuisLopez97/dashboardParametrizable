from backend.models import keyWord
from rest_framework import viewsets, permissions
from .serializers import keyWordSerializer

# KeyWord ViewSet


class KeyViewSet(viewsets.ModelViewSet):
    queryset = keyWord.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = keyWordSerializer
