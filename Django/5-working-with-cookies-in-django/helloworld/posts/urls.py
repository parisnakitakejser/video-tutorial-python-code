from django.urls import path, re_path
from . import views
from .views import PostDetail, PostList

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('set-cookie-demo', views.set_cookie_demo_page, name='index'),
    re_path(r'^(?P<number>\d+)', PostDetail.as_view(), name='post_detail'),
]
