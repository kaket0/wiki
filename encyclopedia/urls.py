from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("article",views.article, name = "article"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/<str:title>",views.wiki, name = "wiki"),
]
