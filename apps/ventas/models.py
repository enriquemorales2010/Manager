from django.db import models
from django.core.exceptions import ValidationError
from apps.inventario.models import Product


class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha", "-created_at"]

    def __str__(self):
        return f"Venta del {self.fecha}"

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.detalleventa_set.all())
        self.save()


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"

    def clean(self):
        if self.cantidad > self.producto.cantidad:
            raise ValidationError(
                f"No hay suficiente stock. Disponible: {self.producto.cantidad}, Solicitado: {self.cantidad}"
            )

    def save(self, *args, **kwargs):
        self.clean()
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.venta.calcular_total()
        self.producto.cantidad -= self.cantidad
        self.producto.save()


def crear_factura(self):
    self.cantidad = 100
    self.precio_unitario = 25
    self.total = self.calcular_total()
    return True

