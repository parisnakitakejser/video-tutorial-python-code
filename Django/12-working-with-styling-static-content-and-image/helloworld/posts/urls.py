from django.urls import path, re_path
from . import views
from .views import PostDetail, PostList, PostSetSessionPage

urlpatterns = [
    path('', PostList.as_view(), name='list-post'),
    path('set-cookie', views.set_cookie_demo_page, name='cookie-page'),
    path('set-session', PostSetSessionPage.as_view(), name='session-page'),
    re_path(r'^(?P<number>\d+)', PostDetail.as_view(), name='post-details'),
]
