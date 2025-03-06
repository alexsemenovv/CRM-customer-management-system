from django.urls import path

from .views import (
    AdsListView,
    AdsCreateView,
    AdsDetailView,
)

app_name = 'adsapp'

urlpatterns = [
    path('', AdsListView.as_view(), name='ads_list'),
    path('new/', AdsCreateView.as_view(), name='ads_create'),
    path('<int:pk>/', AdsDetailView.as_view(), name='ads_detail'),
]
