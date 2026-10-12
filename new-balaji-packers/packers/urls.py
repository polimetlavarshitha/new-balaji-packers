from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('quote/', views.quote, name='quote'),
    path('book/', views.quote, name='book'),
    path('thanks/', views.thanks, name='thanks'),
    path('submit-review/', views.submit_review, name='submit_review'),
]
