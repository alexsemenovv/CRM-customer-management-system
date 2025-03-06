from django.urls import path


from .views import (
    ProductCreate,
    ProductsListView,
)

app_name = "productapp"

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
    path('new/', ProductCreate.as_view(), name='products_create'),
]
