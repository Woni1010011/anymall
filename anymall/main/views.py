from django.shortcuts import render, redirect


def home(request):
    return render(request, "index.html")

def login_email(request):
    return render(request, "login_email.html")

def sign_in(request):
    return render(request, "sign_in.html")

def sign_up(request):
    return render(request, "sign_up.html")

def shop(request):
    return render(request, "shop.html")

def mypage(request):
    return render(request, "mypage.html")

