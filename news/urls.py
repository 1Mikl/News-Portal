from django.urls import path
from .views import (
   PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete
)

urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/',PostDelete.as_view(), name='post_delete'),
]