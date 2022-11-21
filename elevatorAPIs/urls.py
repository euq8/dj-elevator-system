from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from elevatorAPIs import views


urlpatterns = [
    path('requests/', views.RequestsAPIView.as_view()),
    path('requests/<int:elevator_id>/', views.RequestsAPIView.as_view()),
    path('external-request/', views.ExternalRequestAPI.as_view()),
    path('internal-request/', views.InternalRequestAPI.as_view()),
    path('elevator/', views.ElevatorAPI.as_view()),
    path('nextfloor/<int:elevator_id>/', views.NextFloorAPI.as_view()),
    path('direction/<int:elevator_id>/', views.ElevatorDirectionAPI.as_view()),
    path('opendoor/<int:elevator_id>/', views.OpenDoorAPI.as_view()),
    path('closedoor/<int:elevator_id>/', views.CloseDoorAPI.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)