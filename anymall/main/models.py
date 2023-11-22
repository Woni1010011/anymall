from django.db import models

# Create your models here.


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
    
