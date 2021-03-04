from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import GoodRecord,GoodCount
# Create your views here.


def good_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'没登陆呢')
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '对象不存在')

    #点赞处理
    if request.GET.get('is_good') == 'true':
        good_record, created = GoodRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            good_count, created = GoodCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            good_count.good_num +=1
            good_count.save()
            return SuccessResponse(999,good_count.good_num)
        else:
            #有赞了，不能再点了
            return ErrorResponse(402,'已经攒过了')
    else:
        #取消点赞
        if GoodRecord.objects.filter(content_type=content_type, object_id=object_id,user=user).exists():
            good_record = GoodRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            good_record.delete()
            #赞的总数减一
            good_count ,created = GoodCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                good_count.good_num -= 1
                good_count.save()
                return SuccessResponse(4,good_count.good_num)
            else:
                return 'shibai'
        else:
            return ErrorResponse(403,'你 没有攒过咋能取消呢')

def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)
def SuccessResponse(code,message):
    data = { }
    data['status'] = 'SUCCESS'
    data['code'] = code
    data['good_num'] = message
    return JsonResponse(data)