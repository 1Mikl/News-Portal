from django.urls import path
from .views import (
   PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete,
   CategoryListView, subscribe, subscriptions
)

urlpatterns = [
   path('', PostsList.as_view(), name=' '),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

]