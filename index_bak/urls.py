from django.conf.urls import  url
from .views import *

urlpatterns = [
    url('^demo/$', demo_views),
    url('^login/$', login_views),
    url('^regist/$', regist_views),
    url('^', index_views),
]