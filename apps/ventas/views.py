from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db import transaction

from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm, DetalleVentaFormSet


def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, "ventas/venta_list.html", {"ventas": ventas})


def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    detalles = venta.detalleventa_set.all()
    return render(request, "ventas/venta_detail.html", {"venta": venta, "detalles": detalles})


@transaction.atomic
def venta_create(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            venta = form.save()
            formset.instance = venta
            formset.save()
            messages.success(request, "Venta registrada correctamente.")
            return redirect(reverse("ventas:venta_detail", args=[venta.pk]))
    else:
        form = VentaForm()
        formset = DetalleVentaFormSet()
    
    return render(request, "ventas/venta_form.html", {"form": form, "formset": formset})


def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == "POST":
        detalles = venta.detalleventa_set.all()
        for detalle in detalles:
            detalle.producto.cantidad += detalle.cantidad
            detalle.producto.save()
        
        venta.delete()
        messages.success(request, "Venta eliminada y stock restaurado.")
        return redirect(reverse("ventas:venta_list"))
    
    return render(request, "ventas/venta_confirm_delete.html", {"venta": venta})
