from django import forms
from catalog.models import Product, ContactResponse


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'preview_image', 'category', 'price']


class ContactForm(forms.ModelForm):
    class Meta:

        model = ContactResponse
        fields = ['name', 'email']
