from django.urls import path

from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("nuevo/", views.product_create, name="product_create"),
    path("editar/<int:pk>/", views.product_update, name="product_update"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
]
