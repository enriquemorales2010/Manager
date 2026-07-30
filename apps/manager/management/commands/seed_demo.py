from django.core.management.base import BaseCommand

from apps.inventario.models import Product
from apps.ventas.models import DetalleVenta, Venta

PRODUCTOS = [
    ("PAN", "13"),
    ("PAN RELLENO", "4"),
    ("PINITAS", "3"),
    ("Bolita", "4"),
    ("Dulce", "5"),
    ("Tequeños", "5"),
]

STOCK_INICIAL = 10
VENTAS_POR_PRODUCTO = 2
UNIDADES_POR_VENTA = 1


class Command(BaseCommand):
    help = "Carga productos de demo con stock inicial y ventas de ejemplo"

    def handle(self, *args, **options):
        for nombre, precio in PRODUCTOS:
            producto, created = Product.objects.get_or_create(
                nombre=nombre,
                defaults={"precio": precio, "cantidad": STOCK_INICIAL},
            )
            if not created:
                self.stdout.write(f"Ya existe, se omite: {nombre}")
                continue

            for _ in range(VENTAS_POR_PRODUCTO):
                venta = Venta.objects.create()
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=UNIDADES_POR_VENTA,
                    precio_unitario=producto.precio,
                )

            self.stdout.write(self.style.SUCCESS(
                f"{nombre}: stock inicial {STOCK_INICIAL}, "
                f"{VENTAS_POR_PRODUCTO} ventas de {UNIDADES_POR_VENTA} unidad, "
                f"stock restante {producto.cantidad}"
            ))
