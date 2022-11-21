from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from elevatorAPIs.serializers import (
    RequestSerializer as ElevatorRequestSerializer,
    ElevatorSerializer,
)
from elevatorAPIs.models import (
    Request as ElevatorRequest,
    Elevator,
)
from elevatorAPIs.elevator_utils import State, Direction

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class RequestsAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

    # list all uncompleted requests
    def get(self, request, elevator_id=None):
        if elevator_id:
            elevator_requests = ElevatorRequest.objects.filter(elevator_id=elevator_id)
        else:
            elevator_requests = ElevatorRequest.objects.filter(is_completed=False).order_by('id')
        elevator_request_serializer = ElevatorRequestSerializer(elevator_requests, many=True)
        return Response(elevator_request_serializer.data, status=status.HTTP_200_OK)


class ExternalRequestAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['post']
    DATA = {
        'type': 'external',
        'info': {
            'floor': None, # source floor
            'direction': None, # UP or DOWN
        },
        'elevator_id': None,
        'is_completed': False,
    }

    # create an elevator request
    def post(self, request, *args, **kwargs):
        data = {
            'type': 'external',
            'info': {
                'floor': request.data.get('floor'), # source floor
                'direction': request.data.get('direction'), # UP or DOWN
            },
            'elevator_id': request.data.get('elevator_id'),
            'is_completed': False,
        }
        logger.info(data)
        elevator_request_serializer = ElevatorRequestSerializer(data=data)
        if elevator_request_serializer.is_valid():
            elevator_request_serializer.save()
            return Response(elevator_request_serializer.data, status=status.HTTP_201_CREATED)

        return Response(elevator_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InternalRequestAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['post']
    
    # create an elevator request
    def post(self, request, *args, **kwargs):
        data = {
            'type': 'internal',
            'info': {
                'floor': request.data.get('floor') # destination floor
            },
            'elevator_id': request.data.get('elevator_id'),
            'is_completed': False,
        }
        elevator_request_serializer = ElevatorRequestSerializer(data=data)
        if elevator_request_serializer.is_valid():
            elevator_request_serializer.save()
            return Response(elevator_request_serializer.data, status=status.HTTP_201_CREATED)

        return Response(elevator_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElevatorAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post', 'put']
    DATA = {
        'current_floor': 0,
        'current_state': State.IDLE.value,
        'current_direction': Direction.UP.value,
        'is_doors_closed': True,
    }

    def get_elevator_serializer(self, data):
        return ElevatorSerializer(data=data)

    def get(self, request, *args, **kwargs):
        elevators = Elevator.objects.all().order_by('id')
        elevator_serializer = ElevatorSerializer(elevators, many=True)
        return Response(elevator_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        num_of_elevators = request.data.get('total_elevators')
        data = [self.DATA.copy() for _ in range(num_of_elevators)]
        for datum in data:
            elevator_serializer = self.get_elevator_serializer(datum)
            if elevator_serializer.is_valid():
                elevator_serializer.save()
            else:
                return Response(elevator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": f"{num_of_elevators} elevator(s) created successfully."})

    def put(self, request, *args, **kwargs):
        data = self.DATA.copy()
        data['id'] = request.data.get("id")
        data['current_floor'] = request.data.get("floor")
        data['current_state'] = request.data.get("state")
        data['current_direction'] = request.data.get("direction")
        
        elevator = Elevator.objects.get(id=request.data.get("id"))
        elevator_serializer = ElevatorSerializer(data=data)
        if elevator_serializer.is_valid():
            elevator_serializer.update(instance=elevator, validated_data=data)
            return Response(elevator_serializer.data, status=status.HTTP_201_CREATED)
        return Response(elevator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NextFloorAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

    def get(self, request, elevator_id):
        next_floor = None
        elevator = Elevator.objects.get(id=elevator_id)
        current_state = elevator.current_state
        if current_state == State.IDLE.value:
            Response(
                {"message": f"Elevator: {elevator_id} is IDLE."},
                status=status.HTTP_201_CREATED
            )
        current_floor = elevator.current_floor
        current_direction = elevator.current_direction
        requested_floors = [
            elevator_req.info["floor"] for elevator_req in ElevatorRequest.objects.filter(elevator_id=elevator_id)
        ]
        if current_direction == Direction.UP.value:
            requested_floors = sorted(requested_floors)
            for i in requested_floors:
                if i > current_floor:
                    next_floor = i
                    break
        else:
            requested_floors = sorted(requested_floors, reverse=True)
            for i in requested_floors:
                if i < current_floor:
                    next_floor = i
                    break

        if not next_floor:
            # Edge-Case: if there is no floor in the moving 
            # direction, then current floor will be next floor.
            # Though this is not possible in real-life.
            next_floor = current_floor
        
        return Response({"next_floor": next_floor}, status=status.HTTP_201_CREATED)


class ElevatorDirectionAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']
    
    def get(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Exception as err:
            elevator = None

        if not elevator:
            return Response(
                {"message": f"Elevator with id {elevator_id} does not exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"direction": elevator.current_direction}, status=status.HTTP_201_CREATED)


class OpenDoorAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['put']

    def put(self, request, elevator_id):
        elevator = Elevator.objects.get(id=elevator_id)
        data = {
            'current_floor': elevator.current_floor,
            'current_state': elevator.current_state,
            'current_direction': elevator.current_direction,
            'is_doors_closed': False,
        }
        elevator_serializer = ElevatorSerializer(data=data)
        if elevator_serializer.is_valid():
            elevator_serializer.update(instance=elevator, validated_data=data)
            return Response(elevator_serializer.data)
        return Response(elevator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseDoorAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['put']

    def put(self, request, elevator_id):
        elevator = Elevator.objects.get(id=elevator_id)
        data = {
            'current_floor': elevator.current_floor,
            'current_state': elevator.current_state,
            'current_direction': elevator.current_direction,
            'is_doors_closed': True,
        }
        elevator_serializer = ElevatorSerializer(data=data)
        if elevator_serializer.is_valid():
            elevator_serializer.update(instance=elevator, validated_data=data)
            return Response(elevator_serializer.data)
        return Response(elevator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
