from django import forms
from django.core.exceptions import ValidationError
from .models import Venta, DetalleVenta
from apps.inventario.models import Product


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = []


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ["producto", "cantidad", "precio_unitario"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-control producto-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }
        labels = {
            "producto": "Producto",
            "cantidad": "Cantidad",
            "precio_unitario": "Precio Unitario",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["producto"].queryset = Product.objects.filter(disponible=True, cantidad__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get("producto")
        cantidad = cleaned_data.get("cantidad")
        
        if producto and cantidad:
            if cantidad > producto.cantidad:
                raise ValidationError(
                    f"Stock insuficiente para {producto.nombre}. Disponible: {producto.cantidad}, Solicitado: {cantidad}"
                )
        return cleaned_data


DetalleVentaFormSet = forms.inlineformset_factory(
    Venta, DetalleVenta, form=DetalleVentaForm, extra=1, can_delete=True
)
