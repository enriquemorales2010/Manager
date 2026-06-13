from django.urls import path
from . import views

app_name = "manager"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("entradas/", views.entradas, name="entradas"),
    path("analisis/", views.analisis_utilidades, name="analisis_utilidades"),
    path("resumen-ventas/", views.resumen_ventas, name="resumen_ventas"),
]
