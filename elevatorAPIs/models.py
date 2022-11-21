from django.db import models
from elevatorAPIs.elevator_utils import (
    State, Direction, RequestType
)

TOP_FLOOR = 20 # assumption
BOTTOM_FLOOR = -2 # assumption


class Elevator(models.Model):
    id = models.AutoField(primary_key=True)
    current_floor = models.IntegerField()
    current_state = models.CharField(
        max_length=10,
        choices=State.choices(),
        default=(State.IDLE.value, State.IDLE.value),
    )
    current_direction = models.CharField(
        max_length=10,
        choices=Direction.choices(),
        default=(Direction.UP.value, Direction.UP.value),
    )
    is_doors_closed = models.BooleanField(default=True)

    class Meta:
        db_table = "elevators"


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=RequestType.choices())
    info = models.JSONField(blank=False)
    elevator_id = models.ForeignKey(Elevator, to_field="id", on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "requests"
