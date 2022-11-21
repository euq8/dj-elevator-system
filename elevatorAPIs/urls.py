from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from elevator import views


urlpatterns = [
    path('requests/', views.RequestsAPIView.as_view()),
    path('requests/<int:elevator_id>/', views.RequestsAPIView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)