from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View

from shop.models import User
from shop_web.forms.auth_forms import SignInForm, SignUpForm


class SignIn(LoginView):
    template_name = 'sign_in.html'
    authentication_form = SignInForm


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            cleaned_form = form.cleaned_data
            email = cleaned_form.get('email')
            password = cleaned_form.get('password')

            User.objects.create_user(email=email, password=password)
            return redirect('sign-in')

        return render(request, 'sign_up.html', {'form': form})
