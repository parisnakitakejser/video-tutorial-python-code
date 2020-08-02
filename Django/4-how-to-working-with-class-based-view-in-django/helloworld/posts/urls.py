from django.urls import path, re_path
from .views import PostDetail, PostList

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    re_path(r'^(?P<number>\d+)', PostDetail.as_view(), name='post_detail'),
]
