from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.rand, name="random"),
    path("new", views.new, name="new" ),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("<str:entry>", views.search, name="search")
]
