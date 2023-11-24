from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin_set", views.admin_set, name="admin_set"),
    path("shop", views.shop, name="shop"),
    path("mypage", views.mypage, name="mypage"),
]
