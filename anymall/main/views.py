from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *

def home(request):
    # user = CustomUser.objects.get()  # User 대신 CustomUser를 사용합니다.
    return render(request, "index.html")

def login_email(request):
    return render(request, "login_email.html")

def sign_in(request):
    return render(request, "sign_in.html")

def sign_up(request):
    return render(request, "sign_up.html")

def shop(request):

    product = Product.objects.all()

    context = {
        'products':product
    }
    return render(request, "shop.html", context)


def product(request, product_no):
    product = get_object_or_404(Product, product_no=product_no)

    context = {
        'product':product
    }
    return render(request, "product.html", context)

# def mypage(request):
#     # if request.session.get("user_email"):
#     #     user_email = request.session["user_email"]

#     #     try:
#     #         user = User.objects.get(user_email=user_email)
#     #         return render(request, "mypage.html", user)
#     #     except User.DoesNotExist:
#     #         return redirect("home")

#     user = get_object_or_404(CustomUser, user_no=8)  # User 대신 CustomUser를 사용합니다.


#     context = {
#         "user_name" : user.user_name
#     }

#     return render(request, "mypage.html", context)
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

def admin_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category = Category(category_name=category_name)
        category.save()
        return redirect("admin_category")
    else:
        categories = Category.objects.all()
        return render(request, "admin_category.html", {"categories": categories})


def delete_category(request, category_id):
    template = "admin_category.html"
    if request.method == "POST":
        category = Category.objects.get(pk=category_id)

        if Product.objects.filter(category_id=category_id).exists():
            context = {"result": "이 카테고리는 하나 이상의 제품과 연관되어 있어 삭제할 수 없습니다."}
            return render(request, template, context)
        else:
            category.delete()
            return redirect("admin_category")
    else:
        return render(request, template, context)

from django.views.generic.edit import View

def admin_set(request):
    category = Category.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect("shop")
        else:
            print("폼 유효성 검사 실패:", form.errors)
    else:
        form = ProductForm()

    context = {
        'category': category,
        'form': form,
    }

    return render(request, "admin_set.html", context)