from django.db import models


class Product(models.Model):
    nombre = models.CharField("nombre", max_length=150)
    descripcion = models.TextField("descripción", blank=True)
    precio = models.DecimalField("precio", max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField("cantidad en stock", default=0)
    disponible = models.BooleanField("disponible", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre
