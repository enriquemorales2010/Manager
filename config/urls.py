from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.manager.urls")),
    path("inventario/", include("apps.inventario.urls")),    path("ventas/", include("apps.ventas.urls")),]
