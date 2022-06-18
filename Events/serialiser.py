from rest_framework import serializers
from Events.models import Events

class api_event(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"
