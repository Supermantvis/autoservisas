from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = models.OrderComment
        fields = ('content', 'order', 'commenter')
        widgets = {
            'order': forms.HiddenInput(),
            'commenter': forms.HiddenInput(),
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ('plate_number', 'vin_code', 'car_model', 'customer', 'car_img')
        widgets = {
            'customer': forms.HiddenInput(),
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = ('car', 'due_back', 'status')
        widgets = {
            # 'date': DateInput(),
            'due_back': DateInput(),
            'status': forms.HiddenInput(),
        }