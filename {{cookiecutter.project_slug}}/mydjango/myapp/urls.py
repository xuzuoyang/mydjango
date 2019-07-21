from django.urls import re_path

from .views import MyApiView, MyView

myapp_index_urls = [
    re_path('^$', MyView.as_view(), name='myapp_index'),
]

myapp_api_urls = [
    re_path(r'^(?P<app_name>[\w-]+)/?$', MyApiView.as_view(), name='myapp_api')
]
