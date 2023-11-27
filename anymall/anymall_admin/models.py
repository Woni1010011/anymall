from django.db import models

# Create your models here.


class Administrator(models.Model):
    admin_no = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=20, null=False)
    admin_email = models.CharField(max_length=100, null=False)
    admin_password = models.CharField(max_length=100, null=False)
    admin_phone = models.CharField(max_length=11, null=False)
    admin_grade = models.IntegerField(default=1, null=False)
    created_date = models.DateTimeField(default=0, null=False)

    def __str__(self):
        return self.admin_email
