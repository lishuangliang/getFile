import os

from django.shortcuts import render

from .models import *


def demo_views(request):
    return render(request, 'demo.html')

def login_views(request):
    return render(request, 'regist.html')


def check_user_by_phone(request):
    if request.method == 'POST':
        uphone = request.POST.get('uphone')

        user = User.objects.filter(uphone = uphone)



def regist_views(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    else:
        uphone = request.POST.get('uphone')
        uname = request.POST.get('uname')
        upwd = request.POST.get('upwd')

        User.objects.filter()


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


    result_dic = getFile(os.path.join(BASE_DIR, STATIC, curr_path), curr_path, last_path)
    #print(result_dic)
    # return HttpResponse('lalla')
    return render(request, 'index.html', locals())