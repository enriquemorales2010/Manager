from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProductForm
from .models import Product


def product_list(request):
    productos = Product.objects.all()
    return render(request, "inventario/product_list.html", {"productos": productos})


def product_detail(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, "inventario/product_detail.html", {"producto": producto})


def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        producto = form.save()
        messages.success(request, f"Producto '{producto.nombre}' creado correctamente.")
        return redirect(reverse("inventario:product_detail", args=[producto.pk]))

    return render(request, "inventario/product_form.html", {"form": form, "title": "Nuevo producto"})


def product_update(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=producto)
    if request.method == "POST" and form.is_valid():
        producto = form.save()
        messages.success(request, f"Producto '{producto.nombre}' actualizado correctamente.")
        return redirect(reverse("inventario:product_detail", args=[producto.pk]))

    return render(request, "inventario/product_form.html", {"form": form, "title": "Editar producto"})
