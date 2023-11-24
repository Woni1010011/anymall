from django.shortcuts import render, redirect


def home(request):
    return render(request, "index.html")


def shop(request):
    return render(request, "shop.html")


def mypage(request):
    return render(request, "mypage.html")

def admin_set(request):
    return render(request, "admin_set.html")