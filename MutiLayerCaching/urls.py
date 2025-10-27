
from django.urls import path
from .views import get_data

urlpatterns = [
    path('get/<int:id>/', get_data),
]
