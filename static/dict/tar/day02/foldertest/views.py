import json

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *

# Create your views here.
#　http://localhost:8000/login
def login_views(request):
  # 判断　get 请求还是　post　请求
  if request.method == 'GET':
    #get请求　－　判断session,判断cookie,登录页
    #先判断session中是否有登录信息
    if 'uid' in request.session and 'uphone' in request.session:
      #有登录信息保存在　session
      return HttpResponse('您已经登录成功了')
    else:
      #没有登录信息保存在　session，继续判断cookies中是否有登录信息
      if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        #cookies中有登录信息　－　曾经记住过密码
        #将cookies中的信息取出来保存进session，再返回到首页
        uid = request.COOKIES['uid']
        uphone = request.COOKIES['uphone']
        request.session['uid']=uid
        request.session['uphone']=uphone
        return HttpResponse('您已经登录成功')
      else:
        #cookies中没有登录信息　－　去往登录页
        form = LoginForm()
        return render(request,'login.html',locals())
  else:
    #post请求 - 实现登录操作
    #获取手机号和密码
    uphone = request.POST['uphone']
    upwd = request.POST['upwd']
    #判断手机号和密码是否存在(登录是否成功)
    users=User.objects.filter(uphone=uphone,upwd=upwd)
    if users:
      #登录成功：先存进session
      request.session['uid']=users[0].id
      request.session['uphone']=uphone
      #声明响应对象：响应一句话"登录成功"
      resp = HttpResponse("登录成功")
      #判断是否要存进cookies
      if 'isSaved' in request.POST:
        expire = 60*60*24*90
        resp.set_cookie('uid',users[0].id,expire)
        resp.set_cookie('uphone',uphone,expire)
      return resp
    else:
      #登录失败
      form = LoginForm()
      return render(request,'login.html',locals())

# http://localhost:8000/register
def register_views(request):
  # 判断是get请求还是post请求，得到用户的请求意图
  if request.method == 'GET':
    return render(request,'register.html')
  else:
    #先验证手机号在数据库中是否存在
    uphone = request.POST['uphone']
    users = User.objects.filter(uphone=uphone)
    if users:
      #uphone 已经存在
      errMsg = '手机号码已经存在'
      return render(request,'register.html',locals())
    #接收数据插入到数据库中
    upwd = request.POST['upwd']
    uname = request.POST['uname']
    uemail = request.POST['uemail']
    user = User()
    user.uphone = uphone
    user.upwd = upwd
    user.uname = uname
    user.uemail = uemail
    user.save()
    return HttpResponse('注册成功')


# 检查手机号是否已经被注册过
def check_uphone_views(request):
  # 接收前端传递过来的数据 - uphone
  uphone = request.GET['uphone']
  users = User.objects.filter(uphone = uphone)
  if users:
    status = 1
    msg = '手机号码已经存在'
  else:
    status = 0
    msg = '通过'

  dic = {
    'status':status,
    'msg' : msg,
  }
  return HttpResponse(json.dumps(dic))













