from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


app_name = "catalog"

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('contact/info', views.ContactTemplateView.as_view(), name='contact_info'),
    path('contact/form', views.ContactCreateView.as_view(), name='contact_form'),
    path('contact/success', views.ContactSuccessTemplate.as_view(), name='contact_success'),
    path('product/<int:pk>/info', cache_page(60)(views.ProductDetailView.as_view()), name='product_detail'),
    path('product/create', views.ProductCreateView.as_view(), name='product_create'),
    path('product/success_adding', views.ProductSuccessAdding.as_view(), name="product_success"),
    path('product/<int:product_pk>/versions', views.ProductVersionListView.as_view(), name="versions_list"),
    path('product/<int:product_pk>/versions/create', views.ProductVersionCreateView.as_view(), name="version_create"),
    path('product/<int:product_pk>/versions/create/success',
         views.ProductVersionCreateSuccessTemplateView.as_view(),
         name="version_create_success"
         ),
    path('product/<int:product_pk>/versions/<int:version_pk>/update',
         views.ProductVersionUpdateView.as_view(),
         name="version_update"
         ),
    path('product/<int:product_pk>/versions/update/success',
         views.ProductVersionUpdateSuccessTemplateView.as_view(),
         name="version_update_success"
         ),
    path('product/<int:product_pk>/versions/<int:version_pk>/delete',
         views.ProductVersionDeleteView.as_view(),
         name="version_delete"
         ),
    path('product/<int:product_pk>/versions/delete/success',
         views.ProductVersionDeleteSuccessTemplateView.as_view(),
         name="version_delete_success"
         ),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name="product_update"),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name="product_delete")

]


