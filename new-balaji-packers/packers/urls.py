from django.contrib import admin
from django.urls import path, include
from packers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # include other paths like about, contact, quote, sitemap...
]