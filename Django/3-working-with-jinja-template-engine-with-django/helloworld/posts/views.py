from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'post_list.html', {
    })


def post_detail(request, number):
    return render(request, 'post_detail.html', {
        'number': number
    })
