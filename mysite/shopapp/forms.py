from django import forms
from django.core import validators
from django.contrib.auth.models import Group
from django.forms import ModelForm

from shopapp.models import Product, Order


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = 'name',


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    # )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'delivery_address', 'products', 'promocode'



# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(
#         label='Product description',
#         widget=forms.Textarea(attrs={'rows': 5}),
#         validators=[validators.RegexValidator(
#             regex=r'great',
#             message='Поле должно содержать слово great',
#         )],
#     )

