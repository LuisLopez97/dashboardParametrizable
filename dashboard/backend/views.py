from backend.models import Search
from backend.serializers import SearchSerializer
from rest_framework import generics

class SearchListCreate (generics.ListCreateAPIView):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer