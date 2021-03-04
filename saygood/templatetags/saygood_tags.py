from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import GoodRecord, GoodCount


register = template.Library()

@register.simple_tag
def get_good_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    good_count , created = GoodCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
    return good_count.good_num


@register.simple_tag(takes_context=True)
def get_good_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if GoodRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model