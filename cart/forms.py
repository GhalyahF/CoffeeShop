from django import forms
from .models import UserAddress

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = '__all__'
        exclude = ['user']

class AddressSelectForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=UserAddress.objects.all(),
        )
