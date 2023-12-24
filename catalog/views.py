from django.shortcuts import render
from django.urls import reverse_lazy
from catalog.models import Product, ContactResponse
from catalog.forms import ProductForm, ContactForm
from django.views import generic


class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'main'}


class ContactTemplateView(generic.TemplateView):
    template_name = 'catalog/contact_info.html'
    form_class = ContactForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'contact_info'}


class ContactCreateView(generic.CreateView):
    model = ContactResponse
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contact_success')

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'contact_form'}


class ContactSuccessTemplate(generic.TemplateView):
    template_name = 'catalog/contactsuccess.html'


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(generic.CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_success')

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'product_form'}


class ProductSuccessAdding(generic.TemplateView):
    template_name = 'catalog/product_adding_info.html'
