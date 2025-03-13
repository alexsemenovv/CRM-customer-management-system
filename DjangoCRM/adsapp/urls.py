from django.urls import path

from .views import (
    AdsCreateView,
    AdsDeleteView,
    AdsDetailView,
    AdsListView,
    AdsUpdateView,
)

app_name = "adsapp"

urlpatterns = [
    path("", AdsListView.as_view(), name="ads_list"),
    path("new/", AdsCreateView.as_view(), name="ads_create"),
    path("<int:pk>/", AdsDetailView.as_view(), name="ads_detail"),
    path("<int:pk>/edit/", AdsUpdateView.as_view(), name="ads_update"),
    path("<int:pk>/delete/", AdsDeleteView.as_view(), name="ads_delete"),
]
