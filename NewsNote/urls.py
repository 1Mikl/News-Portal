from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls, name='admin'),
   # path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (news/urls.py)
   # подключались к главному приложению с префиксом products/.
   path('news/', include('news.urls')),
]