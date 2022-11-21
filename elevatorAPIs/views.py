from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from elevatorAPIs.serializers import (
    RequestSerializer as ElevatorRequestSerializer,
)
from elevatorAPIs.models import (
    Request as ElevatorRequest,
)

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
