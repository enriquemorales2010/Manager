from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["nombre", "descripcion", "precio", "cantidad", "disponible"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Descripción breve"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "precio": "Precio",
            "cantidad": "Cantidad",
            "disponible": "Disponible",
        }
