from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.shortcuts import render, redirect

from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment
# Create your views here.
def update_comment(request):
    '''
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    #检查提交的数据
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message':'用户没登陆','referer_to':referer })
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message': '没有评论数据', 'referer_to': referer})
    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '这文章对象没了啊', 'referer_to': referer})
    #通过 保存

    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)'''


    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data ={}

    #检测通过保存数据库
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 回复评论的操作
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()

        # 发送邮件通知
        comment.send_mail()


        #返回给当前页面的数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        #data['username'] = comment.reply_to.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%D %H:%M:%S')
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
        #返回 jsonResponse的格式防治页面刷新的效果   return render(request, 'error.html', {'message':comment_form.errors,'redirect_to':reverse})