from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from elevator import views


urlpatterns = [
    path('requests/', views.RequestsAPIView.as_view()),
    path('requests/<int:elevator_id>/', views.RequestsAPIView.as_view()),
    path('external-request/', views.ExternalRequestAPI.as_view()),
    path('internal-request/', views.InternalRequestAPI.as_view()),
    path('elevator/', views.ElevatorAPI.as_view()),
    path('nextfloor/<int:elevator_id>/', views.NextFloorAPI.as_view()),
    path('direction/<int:elevator_id>/', views.ElevatorDirectionAPI.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)