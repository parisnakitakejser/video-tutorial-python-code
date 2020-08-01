from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello world - our first index pages')


def post_detail(request, number):
    return HttpResponse(f'Post detail view pages: {number}')
