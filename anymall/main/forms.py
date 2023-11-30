from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category_id', 'product_name', 'product_price', 'is_option', 'product_thumnail', 'product_description', 'is_display', 'is_for_sale', 'sales_volume']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['sales_volume'].required = False