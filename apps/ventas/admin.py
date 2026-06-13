from django.contrib import admin
from .models import Venta, DetalleVenta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ("subtotal", "created_at")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("pk", "fecha", "total", "created_at")
    list_filter = ("fecha", "created_at")
    search_fields = ("pk",)
    readonly_fields = ("total", "created_at", "updated_at")
    inlines = [DetalleVentaInline]

    fieldsets = (
        ("Información", {"fields": ("fecha", "total")}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("venta", "producto", "cantidad", "precio_unitario", "subtotal")
    list_filter = ("venta__fecha", "producto")
    search_fields = ("producto__nombre", "venta__pk")
    readonly_fields = ("subtotal", "created_at")
