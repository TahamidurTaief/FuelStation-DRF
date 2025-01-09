from django.urls import path
from .views import get_route_with_stops

urlpatterns = [
    path('route/', get_route_with_stops, name='route'),
]
