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
        birth_date = request.POST.get('birth')
        gender = request.POST.get('male_or_female')

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

from django.contrib.auth.decorators import login_required
from django.utils.formats import date_format



@login_required
def mypage(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mypage')  # 프로필이 업데이트된 후 같은 페이지로 리디렉트
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    user = request.user
    context = {
        'form': form,  # 프로필 업데이트 폼 추가
        'user_name': user.username,
        'user_grade': user.grade,
        'sub_date': date_format(user.sub_date, "SHORT_DATE_FORMAT"),
        'user_email': user.email,
        'user_phone': user.user_phone,
        'user_point': user.user_point,
        'user_bank_account':user.refund_bank_name,
        'user_bank_account_num': user.refund_account_number,
        'user_birth': user.birth_date,
        'user_gender': user.gender,
        'user_zipcode': user.zip_code,
        'user_address': user.user_address,
    }
    
    return render(request, 'mypage.html', context)

@login_required
def pwd_verify(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        # USERNAME_FIELD가 'email'로 설정되어 있으므로, email을 사용합니다.
        user = authenticate(email=request.user.email, password=password)
        if user is not None:
            request.session['pwd_verified'] = True
            return redirect('edit_info')
        else:
            messages.error(request, '비밀번호가 틀렸습니다. 다시 입력해주세요.')

    return render(request, 'pwd_verify.html')

@login_required
def edit_info(request):
    if not request.session.get('pwd_verified', False):
        return redirect('pwd_verify')

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            del request.session['pwd_verified']
            messages.success(request, '정보가 업데이트되었습니다.')
            return redirect('mypage')
        else:
            messages.error(request, '입력한 정보가 유효하지 않습니다.')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'edit_info.html', {'form': form})

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
    
def admin_product(request):
    if request.method == "POST":
        product_no = request.POST.get("product_no")
        products = Product(product_no=product_no)
        products.save()
        return redirect("admin_product")
    else:
        products = Product.objects.all()
        return render(request, "admin_product.html", {"products": products})

from django.views.generic.edit import View

def admin_set(request, product_no=None):
    category = Category.objects.all()
    product = None
    
    if product_no:
        product = get_object_or_404(Product, product_no=product_no)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
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

            return redirect("shop", product_no=product.product_no)
        else:
            print("폼 유효성 검사 실패:", form.errors)
    else:
        form = ProductForm(instance=product)

    template = "admin_set.html"
    context = {
        'category': category,
        'form': form,
        'product':product,
        'update_mode': product_no is not None,
        }
    return render(request, template, context)