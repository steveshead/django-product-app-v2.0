from django import forms
from .models import Product
from .models import UserProfile
from django.contrib.admin import widgets
from django.forms import Textarea

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'url', 'product_type', 'price', 'image', 'image_url', 'product_file']
        labels = {
            'name': 'Product Name',
            'url': 'Product URL',
            'product_type': 'Product Type',
            'description': 'Product Description',
            'image': 'Product Image',
            'image_url': 'Product Image URL',
            'price': 'Product Price',
            'product_file': 'Product Zip File',
        }
        widgets = {
            'description': Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        file = self.cleaned_data.get('product_file')

        if file:
            if file._size > 4*1024*1024:
                raise ValidationError("The uploaded file is too large ( > 4mb )")
            if not file.content_type in ["application/zip"]:
                raise ValidationError("Content-Type is not Zip")
            if not os.path.splitext(file.name)[1] in [".zip"]:
                raise ValidationError("Your uploaded file does not have proper extension")
            else:
                pass


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    biography = forms.CharField(label='Biography', widget=Textarea(attrs={'rows': 5}))
    tagline = forms.CharField(label='Tagline', required=False)
    image = forms.ImageField(required=False)


class SubscribeForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)


class ContactForm(forms.Form):
    contact_name = forms.CharField(label="Name", required=True)
    contact_email = forms.EmailField(label="Email", required=True)
    content = forms.CharField(label="Message", required=True, widget=forms.Textarea)
