from django.urls import reverse_lazy, reverse
from catalog.models import Product, ContactResponse, ProductVersion
from catalog.forms import ProductForm, ContactForm, ProductVersionForm
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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

    def get_form(self, form_class=None):
        return self.form_class(initial={'email': self.request.user.email})

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'contact_form'}


class ContactSuccessTemplate(generic.TemplateView):
    template_name = 'catalog/contactsuccess.html'


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'product_form'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect('catalog:product_success')


class ProductSuccessAdding(LoginRequiredMixin, generic.TemplateView):
    template_name = 'catalog/product_adding_info.html'


class ProductVersionListView(LoginRequiredMixin, generic.ListView):
    model = ProductVersion
    context_object_name = "versions"

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_pk"))

    def get_context_data(self, **kwargs):
        context_data = {"product_pk": self.kwargs.get("product_pk")}
        return super().get_context_data(**kwargs) | context_data


class ProductVersionCreateView(LoginRequiredMixin, generic.CreateView):
    model = ProductVersion
    form_class = ProductVersionForm

    def get_success_url(self):
        return reverse("catalog:version_create_success", args=[self.kwargs.get("product_pk")])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product_id = self.kwargs.get("product_pk")
        return super().form_valid(self.object)


class ProductVersionCreateSuccessTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/productversion_success.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"product_pk": self.kwargs.get("product_pk"), "create": True}


class ProductVersionUpdateSuccessTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/productversion_success.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"product_pk": self.kwargs.get("product_pk"), "update": True}


class ProductVersionDeleteSuccessTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/productversion_success.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"product_pk": self.kwargs.get("product_pk"), "delete": True}


class ProductVersionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ProductVersion
    form_class = ProductVersionForm
    pk_url_kwarg = 'version_pk'

    def get_success_url(self):
        return reverse("catalog:version_update_success", args=[self.kwargs.get("product_pk")])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product_id = self.kwargs.get("product_pk")
        self.object.id = self.kwargs.get("version_pk")
        return super().form_valid(self.object)

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_pk"))


class ProductVersionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ProductVersion
    context_object_name = "version"
    pk_url_kwarg = 'version_pk'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"product_pk": self.kwargs.get("product_pk")}

    def get_success_url(self):
        return reverse("catalog:version_delete_success", args=[self.kwargs.get("product_pk")])

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_pk"))


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        product_id = self.kwargs['pk']
        return reverse('catalog:product_detail', kwargs={'pk': product_id})


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    context_object_name = "product"

    def get_success_url(self):
        return reverse('catalog:list')

