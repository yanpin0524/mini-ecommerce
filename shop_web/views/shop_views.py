from django.shortcuts import render


def shop_page(request):
    return render(request, 'layout/base.html')
