from django.urls import path
from . import views


app_name = "catalog"

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('contact_info', views.ContactTemplateView.as_view(), name='contact_info'),
    path('contact_form', views.ContactCreateView.as_view(), name='contact_form'),
    path('contact_success', views.ContactSuccessTemplate.as_view(), name='contact_success'),
    path('product_info/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_form', views.ProductCreateView.as_view(), name='product_form'),
    path('product_success_adding', views.ProductSuccessAdding.as_view(), name="product_success")
]


