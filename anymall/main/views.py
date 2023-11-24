from django.shortcuts import render, redirect
from .models import User

def home(request):
    return render(request, "index.html")


def shop(request):
    return render(request, "shop.html")


def mypage(request):
    if request.session.get("user_email"):
        user_email = request.session["user_email"]

        try:
            user = User.objects.get(user_email=user_email)
            return render(request, "mypage.html", user)
        except User.DoesNotExist:
            return redirect("home")

    return render(request, "mypage.html")
