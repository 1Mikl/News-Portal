from django.contrib import admin
from django.urls import path, include

from news.views import subscriptions

from news.views import subscribe

urlpatterns = [
   path('admin/', admin.site.urls, name='admin'),
   path("accounts/", include("allauth.urls")),
   path('news/', include('news.urls')),
   path('subscriptions/', subscriptions, name='subscriptions'),
   path('subscriptions/<int:pk>/subscribe/', subscribe, name='subscribe'),
]