from django.db import models
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from apps.inventario.models import Product
from apps.ventas.models import Venta, DetalleVenta


def dashboard(request):
    """Dashboard principal con panel de control operativo."""
    productos = Product.objects.all()
    total_productos = productos.count()
    inventario_total = productos.aggregate(total_stock=models.Sum("cantidad"))["total_stock"] or 0
    productos_bajos = productos.filter(cantidad__lte=5).count()
    productos_disponibles = productos.filter(disponible=True).count()
    
    # Datos para tarjetas principales
    ultimas_ventas = Venta.objects.all().order_by("-fecha")[:5]
    total_ventas_hoy = Venta.objects.filter(fecha=timezone.now().date()).count()
    
    # Ganancias del día
    hoy = timezone.now().date()
    detalles_hoy = DetalleVenta.objects.filter(venta__fecha=hoy)
    ganancia_hoy = sum(d.subtotal for d in detalles_hoy) or 0

    context = {
        "total_productos": total_productos,
        "inventario_total": inventario_total,
        "productos_bajos": productos_bajos,
        "productos_disponibles": productos_disponibles,
        "ultimos_productos": productos.order_by("-created_at")[:5],
        "ultimas_ventas": ultimas_ventas,
        "total_ventas_hoy": total_ventas_hoy,
        "ganancia_hoy": ganancia_hoy,
    }
    return render(request, "manager/dashboard.html", context)


def entradas(request):
    """Vista de entradas - últimos productos agregados."""
    productos = Product.objects.all().order_by("-created_at")
    
    context = {
        "productos": productos,
        "total_productos": productos.count(),
    }
    return render(request, "manager/entradas.html", context)


def analisis_utilidades(request):
    """Vista de análisis de utilidades diarias."""
    # Últimos 30 días
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)
    
    # Ventas por día
    ventas_por_dia = {}
    for i in range(30, -1, -1):
        fecha = hoy - timedelta(days=i)
        ventas = Venta.objects.filter(fecha=fecha)
        if ventas.exists():
            detalles = DetalleVenta.objects.filter(venta__fecha=fecha)
            ganancia = sum(d.subtotal for d in detalles) or 0
            ventas_por_dia[fecha.strftime("%d/%m")] = {
                "cantidad": ventas.count(),
                "ganancia": float(ganancia),
            }
    
    # Totales
    ventas_ultimos_30 = Venta.objects.filter(fecha__gte=hace_30_dias)
    detalles_ultimos_30 = DetalleVenta.objects.filter(venta__fecha__gte=hace_30_dias)
    ganancia_total_30 = sum(d.subtotal for d in detalles_ultimos_30) or 0
    promedio_diario = ganancia_total_30 / 30 if ventas_ultimos_30.exists() else 0
    
    context = {
        "ventas_por_dia": ventas_por_dia,
        "ganancia_total_30": float(ganancia_total_30),
        "promedio_diario": float(promedio_diario),
        "total_ventas_30": ventas_ultimos_30.count(),
    }
    return render(request, "manager/analisis_utilidades.html", context)


def resumen_ventas(request):
    """Vista de resumen de ventas por producto y por mes."""
    # Obtener todos los detalles de venta
    detalles = DetalleVenta.objects.select_related('venta', 'producto').order_by('-venta__fecha')
    
    # Estructurar datos: {mes: {producto: {cantidad, ingresos}}}
    ventas_por_mes = defaultdict(lambda: defaultdict(lambda: {"cantidad": 0, "ingresos": 0}))
    
    for detalle in detalles:
        mes_key = detalle.venta.fecha.strftime("%B %Y")  # Ej: "January 2026"
        mes_display = detalle.venta.fecha.strftime("%b %Y")  # Ej: "Jan 2026"
        producto_nombre = detalle.producto.nombre
        
        ventas_por_mes[mes_key][producto_nombre]["cantidad"] += detalle.cantidad
        ventas_por_mes[mes_key][producto_nombre]["ingresos"] += float(detalle.subtotal)
    
    # Convertir a lista ordenada por mes (más reciente primero)
    meses_ordenados = sorted(ventas_por_mes.keys(), reverse=True)
    resumen_final = []
    
    for mes in meses_ordenados:
        productos = ventas_por_mes[mes]
        total_mes = sum(p["ingresos"] for p in productos.values())
        total_items = sum(p["cantidad"] for p in productos.values())
        
        resumen_final.append({
            "mes": mes,
            "productos": sorted(productos.items()),
            "total_ingresos": total_mes,
            "total_items": total_items,
        })
    
    # Totales generales
    total_general_ingresos = sum(mes["total_ingresos"] for mes in resumen_final)
    total_general_items = sum(mes["total_items"] for mes in resumen_final)
    
    # Resumen por producto (todas las ventas)
    resumen_producto = defaultdict(lambda: {"cantidad": 0, "ingresos": 0})
    for mes_data in resumen_final:
        for producto, datos in mes_data["productos"]:
            resumen_producto[producto]["cantidad"] += datos["cantidad"]
            resumen_producto[producto]["ingresos"] += datos["ingresos"]
    
    resumen_producto_ordenado = sorted(resumen_producto.items(), 
                                       key=lambda x: x[1]["ingresos"], 
                                       reverse=True)
    
    # Calcular promedio por venta para cada producto
    resumen_producto_final = []
    for producto, datos in resumen_producto_ordenado:
        promedio = datos["ingresos"] / datos["cantidad"] if datos["cantidad"] > 0 else 0
        resumen_producto_final.append({
            "nombre": producto,
            "cantidad": datos["cantidad"],
            "ingresos": datos["ingresos"],
            "promedio": promedio,
        })
    
    context = {
        "resumen_ventas": resumen_final,
        "resumen_producto": resumen_producto_final,
        "total_general_ingresos": float(total_general_ingresos),
        "total_general_items": int(total_general_items),
        "cantidad_meses": len(resumen_final),
    }
    return render(request, "manager/resumen_ventas.html", context)
