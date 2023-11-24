from django.db import models

# Create your models here.




    # category_id Product reference 아닐 경우 Category 로 edit
class Grade(models.Model):
    grade = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.grade
class User(models.Model):
    user_no = models.AutoField(primary_key=True)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=255)
    user_name = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    user_address = models.TextField(null=True, blank=True)
    user_point = models.IntegerField(default=0)
    is_email = models.BooleanField(default=True)
    sub_date = models.DateField(auto_now_add=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_name
    
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