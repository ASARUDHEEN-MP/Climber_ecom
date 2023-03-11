from django import forms

from category.models import products,Categorys,product_list
from .models import carosuel
from user_app.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = product_list
        fields = ['image','image1','image2','image3', 'name', 'category', 'price', 'description','quantity','slug']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class categoryForm(forms.ModelForm):
    class Meta:
        model = Categorys
        fields = ['image', 'category_name', 'description','slug']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class carosuelForm(forms.ModelForm):
    class Meta:
        model = carosuel
        fields = ['name','image1', 'title','description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            
            
            }
        
        
class orderForm(forms.ModelForm):
    class Meta:
        model = coupon
        fields = ['coupon_code','discount','is_active' ]
        widgets = {
         'coupon_code': forms.TextInput(attrs={'class': 'form-control'}),
          'discount': forms.TextInput(attrs={'class': 'form-control'}),

            
            
            }
