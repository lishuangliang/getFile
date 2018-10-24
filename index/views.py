import json
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from time import time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def demo_views(request):

    return render(request, 'demo.html')

def login_views(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uphone = request.POST.get('uphone')
        upwd=  request.POST.get('upwd')

        user = User.objects.filter(uphone=uphone, upwd=upwd)
        if user:
            # 将成功注册的用户uphone写入session中
            request.session['uphone'] = uphone

            resp = HttpResponse(json.dumps({'code' : 200, 'data' : '', 'msg' : '登录成功'}))
            # 将用户注册手机写入cookies中
            resp.set_cookie('uphone', uphone)

            return resp

        return HttpResponse(json.dumps({'code' : 404, 'data' : '', 'msg' : '用户名或密码不正确'}))

def logout_views(request):
    if 'uphone' in request.session:
        del request.session['uphone']



    return redirect('/')

def check_user_by_phone(request):
    if request.method == 'POST':
        uphone = request.POST.get('uphone')

        user = User.objects.filter(uphone = uphone).first()

        print('check_user_by_phone user -->', user)

        if user:
            return HttpResponse(json.dumps({'code' : 304, 'data' : '', 'msg' : '当前手机号已被注册'}))

        return HttpResponse(json.dumps({'code' : 200, 'data' : '', 'msg' : '当前手机号可以注册'}))



def regist_views(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    else:
        dic = {
            'uphone' : request.POST.get('uphone'),
            'uname' : request.POST.get('uname'),
            'upwd' : request.POST.get('upwd')
        }

        if not(dic['uphone'] and dic['uname'] and dic['upwd']):
            return HttpResponse(json.dumps({'code' : 304, 'data' : '', 'msg' : '注册信息不完全'}))

        user = User(**dic)
        user.save()

        resp = HttpResponse(json.dumps({'code' : 200, 'data' : '', 'msg' : '注册成功'}))

        #将成功注册的用户id, uname写入session中
        request.session['uphone'] = dic['uphone']

        #将用户注册手机写入cookies中
        resp.set_cookie('uphone', dic['uphone'])

        return resp


def update_user(request):
    if request.method == 'GET':
        return render(request, 'update_user.html')
    else:
        if not 'uphone' in request.session:
            return HttpResponse('用户信息丢失')
        uphone = request.session['uphone']
        uname = request.POST.get('uname')

        headimg = request.FILES.get('avatar')
        file_type = headimg.name.split('.')[1]
        headimg.name = uphone +'_headimg.'+ file_type

        print('headimg.name-->', headimg.name)
        user = User.objects.filter(uphone=uphone).first()

        if user:
            if uname:
                user.uname = uname
            user.headimg = headimg
            user.save()

        return redirect('/')


def getFile(filePath, sub_path, last_path):
    if not os.path.exists(filePath):
        return []

    listdir = os.listdir(filePath)

    result = [];
    for i in listdir:
        dic = {}
        dic['filename'] = i

        if os.path.isfile(filePath + '/'+ i):
            dic['filepath'] = os.path.join(sub_path, i)
            dic['filetype'] = os.path.splitext(i)[1][1:]
        else:
            dic['filepath'] = os.path.join(last_path, i)
            dic['filetype'] = 'folder'

        result.append(dic)

    return result


# Create your views here.
def index_views(request):

    if request.path == '/':
        is_home = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC = 'static'

    home_router = '/'

    curr_path = '/'.join(request.path.split('/')[1:])
    sub_path = home_router + '/'.join(request.path.split('/')[1:-1]) or home_router
    last_path = request.path.split('/')[-1]


    #print('curr_path', curr_path)
    #print('next_path', last_path)
    # print('sub_path', sub_path)
    # print(BASE_DIR)

    # print('request.session-->','uphone' in request.session)

    if 'uphone' in request.session:
        curr_user = User.objects.filter(uphone=request.session['uphone']).first()
        # print(type(curr_user.headimg))
        curr_user.avatar = '/' + str(curr_user.headimg)


    result_dic = getFile(os.path.join(BASE_DIR, STATIC, curr_path), curr_path, last_path)


    #print(result_dic)
    # return HttpResponse('lalla')
    return render(request, 'index.html', locals())


def uploadfile(request):
    print('request.path-->',request.path)
    curr_path = request.POST.get('curr_path')
    file = request.FILES.get('file')
    static = 'static'

    if not file:
        return HttpResponse('no file to upload')

    file_to_path = os.path.join(BASE_DIR, static, curr_path, file.name)

    with open(file_to_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    url = request.META.get('HTTP_REFERER', '/')
    return redirect(url)

def createFold(request):
    curr_path = request.POST['curr_path']
    foldname = request.POST['foldname']

    static = 'static'

    folder_path = os.path.join(BASE_DIR, static, curr_path, foldname)

    print('folder_path-->', folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

        url = request.META.get('HTTP_REFERER', '/')
        return redirect(url)

    return HttpResponse('文件夹已存在')


def removeFile(request):

    # todolist

    return HttpResponse('lalala')