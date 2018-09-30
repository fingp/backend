from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads as json_loads
from . import paser
from . import models
from . import posts
from . import forms
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

@csrf_exempt#인증문제 해결
def board(request):
    if request.method == 'POST':
        req = json_loads(request.body.decode("utf-8"))
        data = [{'STATUS': 'SUCCESS'}]
        res = posts.board_list(req)
        data.append(res)
        return JsonResponse(data, safe=False)
    else:
        data = [{'STATUS': 'BoardList_ERROR'}]
        return JsonResponse(data, safe=False)
@csrf_exempt#인증문제 해결
def get_postlist(request):
    if request.method == 'POST':
        req = json_loads(request.body.decode("utf-8"))
        data = [{'STATUS': 'SUCCESS'}]
        res = posts.get_postlist(req)
        data.append(res)
        return JsonResponse(data, safe=False)
    else:
        data = [{'STATUS': 'BoardList_ERROR'}]
        return JsonResponse(data, safe=False)
@csrf_exempt#인증문제 해결
def get_postdetail(request,pk):
    data = [{'STATUS': 'SUCCESS'}]
    res = posts.get_postdetail(pk)
    data.append(res)
    return JsonResponse(data, safe=False)

@csrf_exempt
def comment_add(request, pk):
    if request.method == 'POST':
        form=forms.CommentForm(request.POST)
        if form.is_valid():
            posts.comment_add(form,pk)
            data = [{'STATUS': 'SUCCESS'}]
            return JsonResponse(data, safe=False)
        else:
            data = [{'STATUS': 'FORM ERROR'}]
            return JsonResponse(data, safe=False)
    else:
        data = [{'STATUS': 'COMMENT_NEW ERROR'}]
        return JsonResponse(data, safe=False)