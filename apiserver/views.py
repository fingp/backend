from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads as json_loads
from . import paser

# Create your views here.
@csrf_exempt#인증문제 해결
def post_list(request):
    data = [
        {
            'id': 2014104154,
            'title': 'Operating System',
            'content': 'Practice_01',
            'duedate': '2018.09.19 08:00 - 2018.12.31 23:50',
            'submit': 'N'
        }
    ]
    #data.append(pt())
    return JsonResponse(data, safe=False)

@csrf_exempt#인증문제 해결
def board(request):
    data = [
        {
            'subject': 'BigDataProgramming',
            'author': 'JinHo',
            'date': '2018.09.19 17:52',
            'content': 'Big Data num mo jae mi it Da!'
        }
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt#인증문제 해결
def login(request):
    # TODO request.id , request.password 같은 식으로 로그인 처리
    if request.method=='POST':
        req=json_loads(request.body.decode("utf-8"))
        data = [{'STATUS': 'SUCCESS'}]
        res=paser.login(req)
        data.append(res)
        return JsonResponse(data, safe=False)
    else:
        data = [{'STATUS': 'LOGIN_ERROR'}]
        return JsonResponse(data, safe=False)

@csrf_exempt
def get_assignment(request):
    # 학번 비밀번호 받아서 과제/싸강 긁어오기
    if request.method=='POST':
        req=json_loads(request.body.decode("utf-8"))
        data = [{'STATUS': 'SUCCESS'}]
        res=paser.get_assignment(req)
        data.append(res)
        return JsonResponse(data, safe=False)
    else:
        data = [{'STATUS': 'GET_ASS_ERROR'}]
        return JsonResponse(data, safe=False)
