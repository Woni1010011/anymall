from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *

def home(request):
    # user = CustomUser.objects.get()  # User 대신 CustomUser를 사용합니다.
    return render(request, "index.html")

from django.contrib.auth import authenticate, login
from django.urls import reverse


def login_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '로그인을 성공하였습니다')  # 로그인 성공 메시지
            return redirect('/')
        else:
            messages.error(request, '이메일 또는 비밀번호가 잘못되었습니다')  # 로그인 실패 메시지

    return render(request, 'login_email.html')

def sign_in(request):
    return render(request, "sign_in.html")

from django.contrib import messages
from django.core.exceptions import ValidationError
import re


def validate_password(password):
    """ 간단한 비밀번호 유효성 검사 함수 """
    if len(password) < 8:
        raise ValidationError("비밀번호는 8자 이상이어야 합니다.")
    if not re.search("[a-zA-Z]", password):
        raise ValidationError("비밀번호에는 최소 하나의 문자가 포함되어야 합니다.")
    if not re.search("[0-9]", password):
        raise ValidationError("비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.")

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        password_confirm = request.POST.get('pwd_check')
        user_phone = request.POST.get('phone')
        birth = request.POST.get('birth')  # 추가적인 유효성 검사가 필요할 수 있습니다.
        zip_code = request.POST.get('post_code')
        user_address = request.POST.get('adress')

        # 비밀번호 유효성 검사
        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('sign_up')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('sign_up')

        # 이메일 중복 검사
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, '이미 존재하는 이메일입니다.')
            return redirect('sign_up')

        # 사용자 생성
        user = CustomUser.objects.create_user(
            email=email, 
            username=username, 
            password=password, 
            user_phone=user_phone, 
            zip_code=zip_code, 
            user_address=user_address
        )
        # 생년월일, 우편번호, 주소 추가
        user.birth = birth
        user.zip_code = zip_code
        user.user_address = user_address
        user.save()

        messages.success(request, '회원가입이 성공적으로 완료되었습니다.')
        return redirect('login_email')
    return render(request, 'sign_up.html')

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
            
            for image in request.FILES.getlist('product_images'):
                product_image = ProductImage.objects.create()
                product_image.image = image
                product_image.save()
                product.product_images.add(product_image)

            if form.cleaned_data['is_option']:
                # Get the list of options from the submitted form
                option_names = request.POST.getlist('options-option_name[]')
                option_values = request.POST.getlist('options-option_value[]')
                option_amounts = request.POST.getlist('options-option_amount[]')

                # Create OptionList records for each option
                for name, value, amount in zip(option_names, option_values, option_amounts):
                    print(option_names, option_values, option_amounts)
                    OptionList.objects.create(
                        product_no=product,
                        option_name=name,
                        option_value=value,
                        option_amount=amount,
                    )

            return redirect("shop")
        else:
            print("폼 유효성 검사 실패:", form.errors)
    else:
        form = ProductForm()

    context = {'category': category, 'form': form}
    return render(request, "admin_set.html", context)