from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Post
from .forms import SearchForm, PostForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def news_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'news/news_list.html', {'posts': posts})


def news_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'news/news_detail.html', {'post': post})


def news_search(request):
    form = SearchForm(request.GET)
    posts = Post.objects.all()

    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        date = form.cleaned_data.get('date')

        if title:
            posts = posts.filter(title__icontains=title)
        if author:
            posts = posts.filter(author__user__username__icontains=author)
        if date:
            posts = posts.filter(created_at__gte=date)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)  # 10 новостей на странице
    page = paginator.get_page(page_number)

    return render(request, 'news/news_search.html', {'form': form, 'page': page})


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/add_post.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user.author
        else:
            # Создаем "Неизвестного автора" или используйте дефолтного автора
            unknown_author, created = Author.objects.get_or_create(
                user=User.objects.get(username="Unknown"))
            form.instance.author = unknown_author
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/edit_post.html'  # Создайте этот шаблон
    # После успешного обновления перенаправляем на список новостей
    success_url = reverse_lazy('news_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/delete_post.html'  # Создайте этот шаблон
    success_url = reverse_lazy('news_list')
