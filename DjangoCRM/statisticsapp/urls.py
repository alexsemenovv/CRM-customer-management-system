from django.urls import path

from .views import get_statistics

urlpatterns = [
    path('', get_statistics, name='index'),
]
