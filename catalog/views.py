from django.urls import reverse_lazy, reverse
from catalog.models import Product, ContactResponse, ProductVersion
from catalog.forms import ProductForm, ContactForm, ProductVersionForm
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list) | {'url_name': 'main'}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super().get_queryset().filter(user=self.request.user.id
                                                     ) | super().get_queryset().filter(status="PD")

            if self.request.user.has_perm('catalog.can_moderate'):
                queryset = queryset | super().get_queryset().filter(status="WM")

        else:
            queryset = super().get_queryset().filter(status="PD")

        return queryset


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


class ProductDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Product
    context_object_name = 'product'

    def test_func(self):
        obj = self.model.objects.get(pk=self.kwargs['pk'])
        return obj.status == "PD" or (self.request.user == obj.user
                                      or self.request.user.has_perm("catalog.can_moderate"))

    def get_context_data(self, **kwargs):
        perm_dict = {"can_change": False, "can_delete": False}

        if self.request.user == self.object.user:
            perm_dict['can_delete'] = True
            perm_dict['can_change'] = True

        elif self.request.user.has_perm('catalog.can_moderate'):
            perm_dict['can_change'] = True

        return super().get_context_data(**kwargs) | perm_dict


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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        del form.fields['status']

        return form


class ProductSuccessAdding(LoginRequiredMixin, generic.TemplateView):
    template_name = 'catalog/product_adding_info.html'


class ProductVersionListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = ProductVersion
    context_object_name = "versions"

    def test_func(self):
        obj = Product.objects.get(pk=self.kwargs['product_pk'])
        return obj.status == "PD" or (self.request.user == obj.user
                                      or self.request.user.has_perm("catalog.can_moderate"))

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_pk"))

    def get_context_data(self, **kwargs):
        context_data = {"product_pk": self.kwargs.get("product_pk")}
        return super().get_context_data(**kwargs) | context_data


class ProductVersionCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = ProductVersion
    form_class = ProductVersionForm

    def test_func(self):
        return (self.request.user == Product.objects.get(pk=self.kwargs['product_pk']).user
                or self.request.user.has_perm("catalog.can_moderate"))

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


class ProductVersionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = ProductVersion
    form_class = ProductVersionForm
    pk_url_kwarg = 'version_pk'

    def test_func(self):
        return (self.request.user == Product.objects.get(pk=self.kwargs['product_pk']).user
                or self.request.user.has_perm("catalog.can_moderate"))

    def get_success_url(self):
        return reverse("catalog:version_update_success", args=[self.kwargs.get("product_pk")])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product_id = self.kwargs.get("product_pk")
        self.object.id = self.kwargs.get("version_pk")
        return super().form_valid(self.object)

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_pk"))


class ProductVersionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = ProductVersion
    context_object_name = "version"
    pk_url_kwarg = 'version_pk'

    def test_func(self):
        return (self.request.user == Product.objects.get(pk=self.kwargs['product_pk']).user
                or self.request.user.has_perm("catalog.can_moderate"))

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"product_pk": self.kwargs.get("product_pk")}

    def get_success_url(self):
        return reverse("catalog:version_delete_success", args=[self.kwargs.get("product_pk")])

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_pk"))


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        product_id = self.kwargs['pk']
        return reverse('catalog:product_detail', kwargs={'pk': product_id})

    def test_func(self):
        return (self.request.user == self.model.objects.get(pk=self.kwargs['pk']).user or
                self.request.user.has_perm('catalog.can_moderate'))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.has_perm('catalog.can_moderate'):
            del form.fields['status']

        return form


class ProductDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = Product
    context_object_name = "product"

    def test_func(self):
        return self.request.user == self.model.objects.get(pk=self.kwargs['pk']).user

    def get_success_url(self):
        return reverse('catalog:list')

