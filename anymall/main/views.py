from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *

def home(request):
    # user = CustomUser.objects.get()  # User 대신 CustomUser를 사용합니다.
    return render(request, "index.html")

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse


def login_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.email_verified:
                login(request, user)
                messages.success(request, '로그인을 성공하였습니다.')
                return redirect('/')
            else:
                messages.error(request, '이메일 인증이 필요합니다. 이메일을 확인해 주세요.')
                return render(request, 'login_email.html')  # 로그인 페이지를 다시 보여줍니다.
        else:
            messages.error(request, '이메일 또는 비밀번호가 잘못되었습니다.')
            return render(request, 'login_email.html')  # 로그인 페이지를 다시 보여줍니다.

    return render(request, 'login_email.html')  # 로그인 페이지를 처음 접속했을 때 보여줍니다.

def sign_in(request):
    return render(request, "sign_in.html")

import re
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.signing import TimestampSigner
from django.core.mail import send_mail
from django.conf import settings


def validate_password(password):
    """비밀번호 유효성 검사 함수"""
    if len(password) < 8:
        raise ValidationError("비밀번호는 8자 이상이어야 합니다.")
    if not re.search("[a-zA-Z]", password):
        raise ValidationError("비밀번호에는 최소 하나의 문자가 포함되어야 합니다.")
    if not re.search("[0-9]", password):
        raise ValidationError("비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.")


# views.py
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.http import HttpResponse
from .models import CustomUser

def verify_email(request, token):
    signer = TimestampSigner()
    try:
        email = signer.unsign(token, max_age=86400)  # 24시간 유효
        user = CustomUser.objects.get(email=email)
        user.email_verified = True  # 인증 상태를 True로 변경
        user.save()
        return HttpResponse("이메일 인증이 완료되었습니다!")
    except (BadSignature, SignatureExpired, CustomUser.DoesNotExist):
        return HttpResponse("인증 링크가 유효하지 않거나 만료되었습니다.")


from django.db import IntegrityError

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        password_confirm = request.POST.get('pwd_check')
        user_phone = request.POST.get('phone')
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

        # 사용자 생성
        try:
            user = CustomUser.objects.create_user(
                email=email, 
                username=username, 
                password=password, 
                user_phone=user_phone, 
                zip_code=zip_code, 
                user_address=user_address,
            )
            
            # 이메일 인증 토큰 생성 및 발송
            signer = TimestampSigner()
            token = signer.sign(user.email)
            verification_url = f"{settings.SITE_URL}/verify/{token}/"
            send_mail(
                'Verify your account',
                f'Please click on the link to verify your account: {verification_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, '회원가입이 성공적으로 완료되었습니다. 인증 이메일을 확인해 주세요.')
            return redirect('login_email')

        except IntegrityError:
            messages.error(request, '이미 존재하는 전화번호입니다. 다른 전화번호를 사용해 주세요.')
            return render(request, 'sign_up.html')

    else:
        return render(request, 'sign_up.html')

def shop(request):

    product = Product.objects.all()

    context = {
        'products':product
    }
    return render(request, "shop.html", context)


def product(request, product_no):
    product = get_object_or_404(Product, product_no=product_no)

    options = []
    if product.is_option:
        options = OptionList.objects.filter(product_no=product)

    context = {
        'product': product,
        'options': options,
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
                option_names_add = request.POST.getlist('options-option_name_add[]')
                option_values_add = request.POST.getlist('options-option_value_add[]')
                option_amounts = request.POST.getlist('options-option_amount[]')
                option_stocks = request.POST.getlist('options-option_stock[]')

                # Create OptionList records for each option
                for name, value, name_add, value_add, amount, stock in zip(option_names, option_values, option_names_add, option_values_add, option_amounts, option_stocks):
                    OptionList.objects.create(
                        product_no=product,
                        option_name=name,
                        option_value=value,
                        option_name_add=name_add,
                        option_value_add=value_add,
                        option_amount=amount,
                        option_stock=stock,
                    )

            return redirect("shop")
        else:
            print("폼 유효성 검사 실패:", form.errors)
    else:
        form = ProductForm()

    context = {'category': category, 'form': form}
    return render(request, "admin_set.html", context)