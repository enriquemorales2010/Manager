from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "cantidad", "disponible", "created_at")
    list_filter = ("disponible",)
    search_fields = ("nombre", "descripcion")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("nombre", "descripcion", "precio", "cantidad", "disponible")} ),
        ("Fechas", {"fields": ("created_at", "updated_at")} ),
    )
