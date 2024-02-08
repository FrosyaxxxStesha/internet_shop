from django import forms
from catalog.models import Product, ContactResponse, ProductVersion
from django.conf import settings
from django.forms.widgets import CheckboxInput


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ['name', 'description', 'preview_image', 'category', 'price', 'status']

    def general_field_cleaner(self, field_name, error_message):
        cleaned_data = self.cleaned_data.get(field_name)
        cleaned_data_lower = cleaned_data.lower()

        for word in settings.PRODUCT_FORBIDDEN_WORDS:
            if word in cleaned_data_lower:
                raise forms.ValidationError(error_message)

        return cleaned_data

    def clean_name(self):
        return self.general_field_cleaner('name', 'Запрещенные слова в названии товара')

    def clean_description(self):
        return self.general_field_cleaner('description', 'Запрещённые слова в описании товара')


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ContactResponse
        fields = ['name', 'email']


class ProductVersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input ml-2'
                field.widget.attrs['style'] = 'margin-top: 6px;'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductVersion
        fields = ['name', 'number', 'current']
