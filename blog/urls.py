from django.urls.conf import path
from .views import *


app_name = 'blog'

urlpatterns = [
    path('post/list', PostListView.as_view(), name='post_list'),
    path('post/create', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post/detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post/create/success', PostSuccessCreateTemplateView.as_view(), name='post_create_success'),
    path('post/delete/success', PostSuccessDeleteTemplateView.as_view(), name='post_delete_success'),

]

