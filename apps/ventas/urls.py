from django.urls import path

from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.venta_list, name="venta_list"),
    path("nueva/", views.venta_create, name="venta_create"),
    path("<int:pk>/", views.venta_detail, name="venta_detail"),
    path("<int:pk>/eliminar/", views.venta_delete, name="venta_delete"),
]
