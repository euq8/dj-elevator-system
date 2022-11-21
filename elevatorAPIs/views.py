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


