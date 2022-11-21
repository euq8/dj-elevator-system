from rest_framework import serializers
from elevatorAPIs.models import Request
from elevatorAPIs.models import Elevator


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('type', 'info', 'elevator_id', 'is_completed')


class ElevatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Elevator
        fields = ('id', 'current_floor','current_state','current_direction', 'is_doors_closed')
