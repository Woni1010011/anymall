from django.db import models

# Create your models here.


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


class Stock(models.Model):
    product_no = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="options"
    )
    category_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="categories"
    )
    # category_id Product reference 아닐 경우 Category 로 edit
