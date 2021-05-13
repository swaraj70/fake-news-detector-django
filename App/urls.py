from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('account.urls')),
    path('index', include('detector.urls')),
    path('admin/', admin.site.urls),
]
