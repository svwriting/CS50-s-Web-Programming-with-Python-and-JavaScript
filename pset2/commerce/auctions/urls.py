from django.urls import include, path, re_path

from . import views

from django.views.static import serve
from commerce.settings import MEDIA_ROOT


urlpatterns = [
    path("", views.index, name="index"),
    path("Create", views.create, name="create"),
    path("AddCategory", views.addcategory, name="addcategory"),
    path("Watchlist>", views.watchlist, name="watchlist"),
    path("createdby=<str:username_>", views.indexU, name="indexU"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("Detail/<str:auctionId_>", views.detail, name="detail"),
    path("register", views.register, name="register"),
    path("@<str:auctionId_>", views.index, name="indexD"),
    path("<str:categoryTag_>", views.index, name="indexC"),
    re_path('media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]
