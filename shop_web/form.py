from django import forms
from django.contrib.auth.forms import AuthenticationForm

from shop.models import User


class SignInForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Email or password is incorrect',
    }

    error_class = 'is-invalid'

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'enter your email...',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'enter your password...',
            }
        )
    )


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'enter your password...',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'enter your password again...',
            }
        )
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        error_css_class = 'invalid-feedback'

        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'enter your email...',
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists.')

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Password does not match.')

        return cleaned_data
