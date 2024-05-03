from django.shortcuts import render


def shop_page(request):
    return render(request, 'base.html')
