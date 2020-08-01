from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^\d+', views.post_detail, name='post_detail'),
    re_path(r'^(?P<number>\d+)', views.post_detail, name='post_detail'),
]