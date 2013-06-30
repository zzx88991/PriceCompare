# coding: utf8


from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from PriceCompare.models import Item

import re
import json



def split_list(origin_list, page_len=3):
    '''
    分页切割函数

    @param origin_list: 要切割的原始列表
    @param page_len: 每页包含元素个数

    @return: 页表
    '''

    page_list = []
    i = 0
    while i + page_len <= len(origin_list):
        page_list.append(origin_list[i:i + page_len])
        i += page_len

    if i < len(origin_list):
        page_list.append(origin_list[i:])

    return page_list


@login_required()
def user(request):
    '''
    获取当前用户信息

    @param request: 任意http请求

    @return: 当前用户信息，以JSON格式封装

    '''

    email_hash = ""
    if request.user.is_authenticated():
        email_hash = request.user.userinfo.hash

    user_json = {}
    user_json["email_hash"] = email_hash
    return HttpResponse(json.dumps(user_json))



@login_required()
@csrf_exempt
def favorite(request):
    '''
    为当前用户添加/删除最爱商品

    @param request: POST类型，携带商品ID

    @return: JSON格式，喜爱该商品的用户数量
    '''
    fav_json = {}
    if 'item_id' in request.POST:
        item = get_object_or_404(Item, id=request.POST['item_id'])
        if item in request.user.userinfo.favorite.all():
            request.user.userinfo.favorite.remove(item)
        else:
            request.user.userinfo.favorite.add(item)
        fav_json['fav_num'] = len(item.favorite.all())

    return HttpResponse(json.dumps(fav_json))



@csrf_exempt
def items(request):
    '''
    浏览全部/指定商品

    @param request: POST类型，可选内容有：
                    1. 商品来源 （四家网站）
                    2. 商品排序 （名称或价格）

    @return: HTML文件，包含商品信息列表
    '''

    sort = 'name'
    site = ''

    if 'sort' in request.POST:
        sort = request.POST['sort'].lower()
    if 'site' in request.POST:
        site = request.POST['site'].lower()

    if sort != 'name' and sort != 'price':
        sort = 'name'

    if site == 'taobao':
        site = 't'
    elif site == 'amazon':
        site = 'a'
    elif site == 'jingdong':
        site = 'j'
    elif site == 'dangdang':
        site = 'd'
    elif site == 'favorite':
        site = 'f'
    else:
        site = ''

    if site == '': # 浏览全部商品


        hot_list = Item.objects.order_by('-click_num')
        fresh_list = Item.objects.order_by('-name')

        hot_list = split_list(hot_list, 3)
        fresh_list = split_list(fresh_list, 3)

        return render_to_response('include/tab_panel_home.html', {
            'hot_list': hot_list,
            'fresh_list': fresh_list,
        }, context_instance=RequestContext(request))


    else:

        if site == 'f': # 浏览最爱商品
            item_list = request.user.userinfo.favorite.all()
        else:
            item_list = Item.objects.filter(site=site).order_by('-' + sort)

        page_list = split_list(item_list, 9)

        return render_to_response('include/tab_panel.html', {
            'page_list': page_list,
        }, context_instance=RequestContext(request))


@csrf_exempt
def search(request):
    '''
    搜索商品

    @param request: POST类型，包含查询字符串

    @return: HTML文件，包含查询结果列表


    '''
    item_list = []

    if ('search_query' in request.POST) and request.POST['search_query'].strip():
        search_query = request.POST['search_query']

        sort = 'name'
        if 'sort' in request.POST:
            sort = request.POST['sort'].lower()

        if sort != 'name' and sort != 'price':
            sort = 'name'

        query = get_query(search_query, ['name', ])


        item_list = Item.objects.filter(query).order_by('-' + sort)

    page_list = split_list(item_list, 9)

    return render_to_response('include/tab_panel.html', {
        'page_list': page_list,
    }, context_instance=RequestContext(request))


def get_query(search_query, search_fields):
    '''
    工具函数，用于生成有效的过滤器

    @param search_query: 查询字符串
    @param search_fields: 目标字段（商品名）

    @return: 过滤器，供Item.objects.filter()调用
    '''
    find_terms = re.compile(r'"([^"]+)"|(\S+)').findall # 分词
    norm_space = re.compile(r'\s{2,}').sub

    query = None
    terms = [norm_space(' ', (t[0] or t[1]).strip()) for t in find_terms(search_query)]

    for term in terms:
        or_query = None
        for field in search_fields:
            q = Q(**{"%s__icontains" % field: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query