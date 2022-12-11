from rest_framework import serializers
from studios.models import Studio, Amenities
from classes.models import Class

class StudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Studio
        fields = ('name', 'longitude', 'latitude', 'address', 'distance', 'id')
        
class StudioPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Studio
        fields = ('id', 'name', 'address', 'longitude', 'latitude', 'postal_code', 'phone_number')

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ('studio', 'type')
        extra_kwargs = {'type': {'write_only': True}}

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('studio', 'name', 'coach')
        extra_kwargs = {'name': {'write_only': True}, 'coach': {'write_only': True}}
