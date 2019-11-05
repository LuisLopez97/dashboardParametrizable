from rest_framework import serializers
from backend.models import Search
from backend.models import keyWord

# Serializer permite a Python entender y dar de salida archivos con estructura JSON o XML


class SearchSerializer (serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'

#  Serializer para las palabras claves que se transportaran del frontEnd al backEnd


class keyWordSerializer (serializers.ModelSerializer):
    class Meta:
        model = keyWord
        fields = '__all__'
