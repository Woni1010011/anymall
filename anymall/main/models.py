from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.




    # category_id Product reference 아닐 경우 Category 로 edit
class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    grade = models.CharField(max_length=20, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.grade} - Discount: {self.discount}%"
    
class CustomUser(AbstractUser):
    # AbstractUser에서 username, email, first_name, last_name 등의 필드를 이미 제공하므로 중복되지 않게 주의
    user_no = models.BigAutoField(primary_key=True)
    # email 필드는 AbstractUser에서 제공하므로 추가할 필요 없음
    user_phone = models.CharField(max_length=11, unique=True)
    zip_code = models.IntegerField(null=True, blank=True)
    user_address = models.CharField(max_length=200, null=True, blank=True)
    user_point = models.IntegerField(default=0)
    email_check = models.CharField(max_length=5, null=True, blank=True)
    user_type = models.IntegerField(null=True, blank=True)
    sub_date = models.DateTimeField(auto_now_add=True)
    # Grade 모델을 참조하는 외래 키
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    
class Category(models.Model) :
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    pass

    
class Product(models.Model) :
    product_no = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField(default=0)
    is_option = models.BooleanField(default=True)
    product_date = models.DateField(auto_now_add=True)
    product_thumnail = models.ImageField(upload_to='product_thumnails/')
    product_description = models.TextField(1000)
    product_images = models.ManyToManyField('ProductImage', related_name='product_images')
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

class ProductImage(models.Model) :
    image = models.ImageField(upload_to='product_images/')

    def __str__(self) :
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