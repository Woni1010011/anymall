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
        
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'user_phone', 'new_password1', 'new_password2', 'profile_picture')

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['new_password1']:
            user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user


        
