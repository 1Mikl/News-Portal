from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import PostForm
from .models import *
from datetime import datetime
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)

DEFAULT_FROM_EMAIL = "Zela52@yandex.ru"


# Create your views here.
class PostsList(ListView):

    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 3  # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "СКИДКА на новостную подписку уже завтра!"
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
    queryset = Post.objects.all()


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        # context['next_sale'] = "СКИДКА на новостную подписку уже завтра!"
        return context


    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj, 5)

        return obj

class PostSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news_search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class CategoryListView(PostsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk']) #получили 1 категорию
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation') #(queryset)набор запросов к 1 категории
        return queryset #все статьи к этой категории

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscribers.add(user)


    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'postCategory': postCategory, 'message': message})




from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscriber, Category


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':

        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

