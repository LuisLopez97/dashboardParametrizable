from rest_framework import serializers
from DB.models import Busquedas

# Busquedas Serializer


class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busquedas
        fields = '__all__'
