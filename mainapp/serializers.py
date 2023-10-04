from rest_framework import serializers
from .models import PetroleumData

class PetroleumDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetroleumData
        fields = '__all__'

