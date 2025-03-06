from django.urls import path


from .views import (
    ProductCreateView,
    ProductsListView,
    ProductDetailsView,
)

app_name = "productapp"

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
    path('new/', ProductCreateView.as_view(), name='products_create'),
    path('<int:pk>/', ProductDetailsView.as_view(), name='products_detail'),
]
