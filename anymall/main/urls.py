from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin_set", views.admin_set, name="admin_set"),
    path("product_update/<int:product_no>/", views.admin_set, name="admin_set"),
    path("admin_category", views.admin_category, name="admin_category"),
    path("admin_product", views.admin_product, name="admin_product"),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path("shop", views.shop, name="shop"),
    path('product/<int:product_no>/', views.product, name="product"),
    path("mypage", views.mypage, name="mypage"),
    path('pwd_verify/', views.pwd_verify, name='pwd_verify'),
    path('edit_info/', views.edit_info, name='edit_info'),
    path("login_email", views.login_email, name="login_email"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_up", views.sign_up, name="sign_up"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('social-auth/', include('social_django.urls', namespace='social')),

]
