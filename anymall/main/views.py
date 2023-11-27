from django.shortcuts import render, redirect, get_object_or_404
from .models import User

def home(request):
    user = User.objects.get()
    return render(request, "index.html")

def login_email(request):
    return render(request, "login_email.html")

def sign_in(request):
    return render(request, "sign_in.html")

def sign_up(request):
    return render(request, "sign_up.html")

def shop(request):
    return render(request, "shop.html")
def product(request):
    return render(request, "product.html")

def mypage(request):
<<<<<<< HEAD
    return render(request, "mypage.html")

=======
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
>>>>>>> main
