from rest_framework import serializers
from .models import TruckStop

class TruckStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckStop
        fields = '__all__'
