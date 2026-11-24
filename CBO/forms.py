from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'     #instead of choosing one by one
        labels = {
            'name': 'Clothing Item Name',
            'category': 'Apparel Category',
            'size': 'Available Size',
            'color': 'Color / Variant',
            'price': 'Price (KES)',
            'stock': 'Stock Quantity',
            'description': 'Fabric & Style Details',
            'image': 'Product Photo',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Men Slim-Fit Cotton Shirt'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select form-control'
            }),

            'size': forms.Select(attrs={
                'class': 'form-select form-control'
            }),

            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Navy Blue, Black, White'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price in KES (e.g., 1500)',
                'min': '0',
                'step': '0.01'
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter available quantity (e.g., 25)',
                'min': '0'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe material (e.g., 100% Cotton), fit, and care instructions...'
            }),
            
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    # class RegisterForm(UserCreationForm):
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta:
        model = User
        fields = ['username', 'email']

        