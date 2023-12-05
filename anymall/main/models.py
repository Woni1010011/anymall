from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    # 필수로 필요한 데이터를 선언
    def create_user(self, email, username, password=None, user_phone=None, zip_code=None, user_address=None):
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email=email, 
            username=username, 
            password=password, 
            user_phone=user_phone,
            zip_code=zip_code,
            user_address=user_address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, username, password=None):
        user = self.create_user(email=email, username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # AbstractUser에서 username, email, first_name, last_name 등의 필드를 이미 제공하므로 중복되지 않게 주의
    user_no = models.BigAutoField(primary_key=True)
    username = models.CharField("사용자 이름", max_length=20, unique=True)
    password = models.CharField("비밀번호", max_length=128)  # 해시되기 때문에 max_length가 길어야함
    email = models.EmailField("사용자 계정", max_length=100, unique=True)
    user_phone = models.CharField(max_length=11, unique=True)
    zip_code = models.IntegerField(null=True, blank=True)
    user_address = models.CharField(max_length=200, null=True, blank=True)
    user_point = models.IntegerField(default=0)
    email_check = models.CharField(max_length=5, null=True, blank=True)
    email_verified =models.BooleanField(default=False)
    verification_code =models.CharField(max_length=6, null=True, blank=True)
    user_type = models.IntegerField(default=0, blank=True)
    sub_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(default="Bronze", max_length=20, null=False)
    refund_bank_name = models.CharField(max_length=50, null=True, blank=True) # 환불 은행 이름
    refund_account_number = models.CharField(max_length=50, null=True, blank=True) # 환불 계좌 번호
    birth_date = models.DateField(null=True, blank=True) # 사용자가 이 필드를 비워둘 수 있습니다.
    gender = models.CharField(max_length=10, choices=(('male', '남자'), ('female', '여자')), null=True, blank=True) # 이 필드도 선택적입니다.


    # 관리자 권한 여부 (기본값은 False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 실제 로그인에 사용되는 아이디
    USERNAME_FIELD = "email"

    # 어드민 계정을 만들 때 입력받을 정보 ex) email
    # 사용하지 않더라도 선언이 되어야함
    # USERNAME_FIELD와 비밀번호는 기본적으로 포함되어있음
    REQUIRED_FIELDS = ["username"]
    # custom user 생성 시 필요
    objects = UserManager()

    # # 어드민 페이지에서 데이터를 제목을 어떻게 붙여줄 것인지 지정
    # def __Str__(self):
    #     return f"{self.username} / {self.email} 님의 계정입니다"

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    # 일반적으로 선언만 해두고 건들지않는다
    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    pass


class Product(models.Model):
    product_no = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField(default=0)
    is_option = models.BooleanField(default=True)
    product_date = models.DateField(auto_now_add=True)
    product_thumnail = models.ImageField(upload_to="product_thumnails/")
    product_description = models.TextField(1000)
    product_images = models.ManyToManyField(
        "ProductImage", related_name="product_images"
    )
    is_display = models.BooleanField(default=True)
    is_for_sale = models.BooleanField(default=True)
    sales_volume = models.IntegerField(default=0)

    pass


class Stock(models.Model):
    product_no = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stocks"
    )
    category_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="categories"
    )


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image {self.id}"


class OptionList(models.Model):
    option_no = models.AutoField(primary_key=True)
    product_no = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="options"
    )
    option_name = models.CharField(max_length=20, null=False)
    option_value = models.CharField(max_length=20, null=False)
    option_amount = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.option_name
