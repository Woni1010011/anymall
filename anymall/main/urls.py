from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop", views.shop, name="shop"),
    path("mypage", views.mypage, name="mypage"),
    path("login_email", views.login_email, name="login_email"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_up", views.sign_up, name="sign_up"),

]
