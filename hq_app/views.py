from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    return  render(request,'home.html',context)

