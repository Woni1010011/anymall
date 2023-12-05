from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category_id', 'product_name', 'product_price', 'is_option', 'product_thumnail', 'product_description', 'is_display', 'is_for_sale', 'sales_volume', 'total_stock']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sales_volume'].required = False
    
    # Add option_name, option_value, and option_amount fields
    option_name = forms.CharField(max_length=20, required=False)
    option_value = forms.CharField(max_length=20, required=False)
    option_amount = forms.IntegerField(required=False)
    
    option_name_add = models.CharField(max_length=20)
    option_value_add = models.CharField(max_length=20)
    option_stock = models.IntegerField

    # Add prefix to option fields to handle multiple options
    def add_prefix(self, field_name):
        if field_name in ['option_name', 'option_value', 'option_amount','option_name_add','option_value_add','option_stock']:
            return f'options-{field_name}'
        return super().add_prefix(field_name)
    
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'user_phone', 'zip_code', 'user_address')
