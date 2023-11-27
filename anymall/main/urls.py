from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin_set", views.admin_set, name="admin_set"),
    path("admin_category", views.admin_category, name="admin_category"),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path("shop", views.shop, name="shop"),
    # path("product", views.product, name="product"),
    path('product/<int:product_no>/', views.product, name="product"),
    path("mypage", views.mypage, name="mypage"),
    path("login_email", views.login_email, name="login_email"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_up", views.sign_up, name="sign_up"),

]
