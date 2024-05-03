from django import forms
from django.core.exceptions import ValidationError

from medical_services.models import Service, Category, Cart


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ("category_title", "category_description", "category_image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ServicesForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ("services_title", "services_description", "category", "price", "deadline",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CartForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ("services", "date", "client",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'