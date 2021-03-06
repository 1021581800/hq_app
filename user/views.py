import string
import random
import time

from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from user.models import Profile

from .forms import LoginForm, RegForm, ChangeNicknameForm,BindEmailForm
from django.shortcuts import  redirect,render
from django.urls import reverse
from django.core.mail import send_mail

def login(request):
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username,password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request,'error.html',{'message':'用户或密码错误噢'})
'''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user =login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form= LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'user/login.html', context)
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)
def register(request):
    if request.method == 'POST':
        register_form = RegForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']

            #创建用户
            user = User.objects.create_user(username,None,password)
            user.save()
            #登陆
            user = auth.authenticate(username=username,password=password)
            auth.login(request, user)

            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegForm()
    context = { }
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)




def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '确定改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context )


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/email.html', context )


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '1021581800@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)