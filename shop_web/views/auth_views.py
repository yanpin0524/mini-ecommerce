from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from shop.models import User
from shop_web.form import SignUpForm


class SignInView(View):
    def get(self, request):
        return render(request, 'sign-in.html')


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            cleaned_form = form.cleaned_data
            email = cleaned_form.get('email')
            password = cleaned_form.get('password')

            User.objects.create_user(email=email, password=password)
            return HttpResponseRedirect('/sign-in/')

        return render(request, 'sign-up.html', {'form': form})
