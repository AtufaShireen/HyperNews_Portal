from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('news/<int:link>/', views.NewsView.as_view()),
    path('news/', views.MainView.as_view(), name='news'),
    path('news/create/', views.AddView.as_view(), name='addnews'),
]
