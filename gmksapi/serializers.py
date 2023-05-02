from rest_framework import serializers

from .models import *

class DataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField() # Here
    class Meta:
        model = Data
        fields = ('id','loc', 'category','upload')
        extra_kwargs = {'id': {'read_only': False}}


    def create(self, validated_data):
        return Data.objects.create(validated_data)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = "__all__"
    def create(self, validated_data):
        return Data.objects.create(validated_data)


class AwarenessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Awareness
        fields = ('id','event','loc', 'date','time','file')

    def create(self, validated_data):
        return Data.objects.create(validated_data)
