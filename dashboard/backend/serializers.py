from rest_framework import serializers
from backend.models import Search
from backend.models import keyWord


class SearchSerializer (serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'


class keyWordSerializer (serializers.ModelSerializer):
    class Meta:
        model = keyWord
        fields = '__all__'
