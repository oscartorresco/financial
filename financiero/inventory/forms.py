from django.forms import ModelForm
from django import forms
from inventory.models import Producto

class ProductForm(ModelForm):
    class Meta:
        model = Producto