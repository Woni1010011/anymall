from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Product

def home(request):
    user = User.objects.get()
    return render(request, "index.html")


def shop(request):

    product = Product.objects.all()

    context = {
        'products':product
    }
    print(context)
    return render(request, "shop.html", context)


def product(request):
    return render(request, "product.html")


def mypage(request):
    # if request.session.get("user_email"):
    #     user_email = request.session["user_email"]

    #     try:
    #         user = User.objects.get(user_email=user_email)
    #         return render(request, "mypage.html", user)
    #     except User.DoesNotExist:
    #         return redirect("home")

    user = get_object_or_404(User, user_no=8)


    context = {
        "user_name" : user.user_name
    }

    return render(request, "mypage.html", context)


def admin_set(request):
    return render(request, "admin_set.html")
