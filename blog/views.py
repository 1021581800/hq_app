from django.db.models import Count
from django.shortcuts import get_object_or_404,render
from .models import Blog,BlogType
from django.core.paginator import Paginator
from read_statistics.utils import read_statistics_once_read

# Create your views here.

def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, 6)  # 每几篇文章进行分类。
    page_num = request.GET.get('page', 1)  # 获取get的请求页数
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number  # 当前页码
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 上面是获取当前页码前后两个，防止出现-1，超出页码数的情况

    # 省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '....')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('....')

    # 首页和尾页的现实
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    '''
        blog_types = BlogType.objects.all()
        blog_type_list = []
        for blog_type in blog_types:
            blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
            blog_type_list.append(blog_type)
            blog_type_list= B
    '''
    #  日期数量博客
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict ={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month =blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):



    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    return render(request,'blog_list.html', context)
def blog_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blogs_with_type.html',context)
def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context= get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request,'blogs_with_date.html', context)
def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)


    context = {}
    #加载评论
    # 回复评论内容


    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog

    response = render(request, 'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response

def blog_list_type(request,blog_type):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render(request,'blog_list_type.html', context)

