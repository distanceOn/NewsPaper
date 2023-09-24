from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Post, Category
from .forms import SearchForm, PostForm
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .mixins import AuthorPermissionMixin
from .models import Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def news_list(request):
    posts = Post.objects.order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'news/news_list.html', {'posts': posts, 'categories': categories})


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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/add_post.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            author, created = Author.objects.get_or_create(
                user=self.request.user)
            form.instance.author = author
        else:
            form.instance.author = None

        # Сохраняем пост
        response = super().form_valid(form)

        # Отправляем уведомление о создании поста подписчикам категории
        if form.cleaned_data.get('categories'):
            for category in form.cleaned_data['categories']:
                send_newsletter_notification(category, self.object)

        return response


class AuthenticatedMixin(LoginRequiredMixin, AuthorPermissionMixin):
    login_url = '/accounts/login/'


class PostUpdateView(LoginRequiredMixin, AuthorPermissionMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/edit_post.html'
    success_url = reverse_lazy('news_list')


class PostDeleteView(LoginRequiredMixin, AuthorPermissionMixin,DeleteView):
    model = Post
    template_name = 'news/delete_post.html'
    success_url = reverse_lazy('news_list')





@login_required
def become_author(request):
    authors_group, created = Group.objects.get_or_create(name='authors')
    request.user.groups.add(authors_group)
    return redirect('/news/')  


def subscribe_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    user = request.user

    if user not in category.subscribers.all():
        category.subscribers.add(user)

    return redirect('news_list')

def unsubscribe_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    user = request.user

    if user in category.subscribers.all():
        category.subscribers.remove(user)

    return redirect('news_list')

def send_newsletter_notification(category, post):
    subscribers = category.subscribers.all()

    for user in subscribers:
        subject = post.title if post else "Новая статья в твоём любимом разделе!"
        
        # Рендерим HTML-содержимое из шаблона
        html_content = render_to_string('news/newsletter.html', {'post': post, 'user': user})

        # Создаем EmailMultiAlternatives объект
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',  # Вы можете оставить body пустым, так как у нас есть HTML-содержимое
            from_email='distanceOn@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")  # Добавляем HTML-содержимое

        # Отправляем письмо
        msg.send()