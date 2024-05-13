from django import forms

from shop.models import CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

        widgets = {
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control form-control-sm', 'min': 1, 'value': 1}
            )
        }
