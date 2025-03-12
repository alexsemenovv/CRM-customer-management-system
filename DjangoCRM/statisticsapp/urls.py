from django.urls import path

from .views import get_statistics

app_name = "statisticsapp"

urlpatterns = [
    path('', get_statistics, name='index'),
]
