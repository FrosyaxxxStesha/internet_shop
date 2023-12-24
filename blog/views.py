
from .models import Post
from django.views import generic
from .forms import PostModelForm
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify


class PostListView(generic.ListView):
    model = Post
    paginate_by = 3
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs) | {'url_name': 'post_list'}

    def get_queryset(self):
        queryset = super().get_queryset()
        new_queryset = queryset.filter(published=True)
        return new_queryset


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.post = super().get_object(queryset)
        self.post.views += 1
        self.post.save()
        return self.post


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostModelForm
    success_url = reverse_lazy('blog:post_create_success')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.slug = slugify(obj.title)
        obj.published = True
        obj.save()
        return super().form_valid(form)


class PostSuccessCreateTemplateView(generic.TemplateView):
    template_name = 'blog/successes/create.html'


class PostUpdateView(generic.UpdateView):
    model = Post
    context_object_name = 'post'
    form_class = PostModelForm

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse('blog:post_detail', kwargs={'pk': post_id})


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_delete_success')


class PostSuccessDeleteTemplateView(generic.TemplateView):
    template_name = 'blog/successes/delete.html'
