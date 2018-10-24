from django.conf.urls import  url
from .views import *

urlpatterns = [
    url('^demo/$', demo_views),
    url('^login/$', login_views),
    url('^regist/$', regist_views),
    url('^logout/$', logout_views),
    url('^check_user_by_phone/$', check_user_by_phone),
    url('^update_user/$', update_user),
    url(r'^uploadfile/$', uploadfile),
    url(r'^createFold/$', createFold),
    url(r'^removeFile/$', removeFile),
    url('^', index_views),
]