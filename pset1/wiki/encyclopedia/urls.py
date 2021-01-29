from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("@CreateNewPage", views.create, name="crate"),
    path("@RandomPage", views.randompage, name="random"),
    path("@Edit<str:TITLE>", views.edit, name="edit"),
    path("<str:TITLE>", views.index, name="entry")
]
