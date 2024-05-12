from django import forms

from shop.models import User


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
