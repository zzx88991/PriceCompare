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
import urllib
from BeautifulSoup import BeautifulSoup


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

    @return: JSON格式，包含收藏该商品的用户数量、当前用户是否收藏该商品
    '''
    fav_json = {}
    if 'item_id' in request.POST:
        item = get_object_or_404(Item, id=request.POST['item_id'])
        if item in request.user.userinfo.favorite.all():
            request.user.userinfo.favorite.remove(item)
        else:
            request.user.userinfo.favorite.add(item)
        fav_json['fav_num'] = len(item.favorite.all())
        fav_json['is_fav'] = item in request.user.userinfo.favorite.all()

    return HttpResponse(json.dumps(fav_json))




@csrf_exempt
def search(request):
    '''
    处理用户搜索请求
    1、查询字符串不为空时，执行搜索
    2、查询字符串为空时，执行浏览

    @param request: POST类型，包含查询字符串、查询每页条数、价格区间、排序依据、来源站点、是否查询收藏夹

    @return: HTML文件，包含查询结果列表


    '''
    item_list = []

    search_query = ''
    if ('search_query' in request.POST) and request.POST['search_query'].strip():
        search_query = request.POST['search_query']


    num = 9
    if 'num' in request.POST:
        num = abs(int(request.POST['num'].lower()))
    if num % 3 != 0:
        num -= num % 3
    if num == 0:
        num = 9


    price_low = 0
    if 'price_low' in request.POST:
        price_low = abs(int(request.POST['price_low'].lower()))
    price_high = 999999999
    if 'price_high' in request.POST:
        price_high = abs(int(request.POST['price_high'].lower()))

    if price_low > price_high:
        price_low = 0
        price_high = 999999999

    check_fav = 'false'
    if 'check_fav' in request.POST:
        check_fav = request.POST['check_fav'].lower()
    if check_fav != 'true' and check_fav != 'false':
        check_fav = 'false'

    sort = 'name'
    if 'sort' in request.POST:
        sort = request.POST['sort'].lower()
    if sort != 'name' and sort != 'price' and sort != '-price':
        sort = 'name'


    site = ''
    if 'site' in request.POST:
        site = request.POST['site'].lower()
    if site == 'taobao':
        site = 't'
    elif site == 'amazon':
        site = 'a'
    elif site == 'jingdong':
        site = 'j'
    elif site == 'dangdang':
        site = 'd'
    else:
        site = ''

    # POST信息处理完毕，开始处理

    #按价格区间排序
    item_list = Item.objects.filter(price__range=[price_low, price_high])

    if check_fav == 'true': # 浏览最爱商品
        item_list = item_list.filter(favorite=request.user.userinfo)

    if search_query != '': # 用户请求本地检索
        query = get_query(search_query, ['name', ])
        item_list = item_list.filter(query)


    if site != '': # 浏览指定站点商品
        item_list = item_list.filter(site=site)


    # 排序
    item_list = item_list.order_by(sort)[:100]
    # 分割
    page_list = split_list(item_list, num)

    return render_to_response('include/tab_panel.html', {
        'page_list': page_list,
        'site': site,
        'total_item_num': len(item_list)
    }, context_instance=RequestContext(request))


def get_query(search_query, search_fields):
    '''
    工具函数，服务于search()，用于生成有效的过滤器

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

@csrf_exempt
def update(request):
    '''
    使用用户提供的关键字检索互联网以更新数据库，
    更新完毕后发送特殊回复

    @param request: POST类型，包含查询字符串和互联网查询页数

    @param return: 状态号222,表示更新结束
    '''

    search_query = ''
    if ('search_query' in request.POST) and request.POST['search_query'].strip():
        search_query = request.POST['search_query']

    search_page = 0
    if 'search_page' in request.POST:
        search_page = abs(int(request.POST['search_page'].lower()))

    if search_query != '':
        search_t(search_query, search_page)
        search_a(search_query, search_page)
        search_j(search_query, search_page)
        return HttpResponse(status='222')



def search_t(query, page_num):
    '''
    抓取淘宝数据
    1、注意URL参数
    2、注意动态加载的隐藏商品
    3、注意编码
    '''
    query_url = ('http://s.taobao.com/search?tab=all&cd=false&dc=1&q='+query+'&s='+str(60*page_num)).encode('utf8')
    page = urllib.urlopen(urllib.unquote(query_url)).read()
    soup = BeautifulSoup(''.join(page), fromEncoding="GB18030")

    # 第一层：非隐藏的几个商品
    first_list = soup.findAll('div', {'class': re.compile('item')})

    # 第二层：隐藏的多个商品
    lazy_area = soup.find('textarea', {'class': re.compile('datalazyload')})
    soup = BeautifulSoup(''.join(lazy_area.contents[0]))
    second_list = soup.findAll('div', {'class': re.compile('item')})

    item_list = first_list + second_list


    for item in item_list:
        # 提取图片地址
        img = item.find('img')['src']
        # 提取商品名称
        name = item.find('h3').find('a')['title']
        # 提取商品链接
        url = item.find('h3').find('a')['href']
        # 提取商品价格
        price = re.compile('\d*\.\d*').findall(item.find('div', {'class': re.compile('price')}).contents[0])[0]
        new_item = Item.objects.get_or_create(url=url)[0]
        new_item.name = name
        new_item.price = price
        new_item.img = img
        new_item.site = 't'
        if new_item != None:
            print '一个野生的淘宝商品被加入了！'
        new_item.save()




def search_a(query, page_num):
    '''
    抓取亚马逊数据
    1、注意网址选取
    2、注意判断价格是否存在
    '''
    query_url = ('http://www.amazon.cn/s/field-keywords='+query+'&page='+str(page_num+1)).encode('utf8')
    page = urllib.urlopen(urllib.unquote(query_url)).read()
    soup = BeautifulSoup(''.join(page))

    item_list = soup.findAll('div', {'id': re.compile('result_')})

    for item in item_list:
        # 提取图片地址
        img = item.find('a').find('img')['src']

        title_div = item.find('div', {'class': re.compile('productTitle')})
        if title_div != None:
            # 提取商品名称
            name = title_div.find('a').contents[0]
            # 提取商品链接
            url = title_div.find('a')['href']

        price_div = item.find('div', {'class': re.compile('newPrice')})
        if price_div != None:
            # 提取商品价格
            price = re.compile('\d*\.\d*').findall(price_div.find('span').contents[0])[0]

        new_item = Item.objects.get_or_create(url=url)[0]
        new_item.name = name
        new_item.price = price
        new_item.img = img
        new_item.site = 'a'
        if new_item != None:
            print '一个野生的亚马逊商品被加入了！'
        new_item.save()


def search_j(query, page_num):
    '''
    抓取京东数据
    1、注意编码
    2、价格信息动态加载，需要读取特定URL获取
    3、标题中含有TAG，需要二级访问页面
    '''
    query_url = ('http://search.jd.com/Search?enc=utf-8&keyword='+query+'&page='+str(page_num+1)).encode('utf8')
    page = urllib.urlopen(urllib.unquote(query_url)).read()
    soup = BeautifulSoup(''.join(page), fromEncoding="GB18030")

    item_list = soup.findAll('li', {'sku': re.compile('\d*')})

    for item in item_list:

        # 提取图片地址
        img = item.find('img')['data-lazyload']

        # 提取商品链接
        url = item.find('div', {'class': re.compile('p\-name')}).find('a')['href']


        # 提取商品名称
        page = urllib.urlopen(urllib.unquote(url)).read()
        soup = BeautifulSoup(''.join(page), fromEncoding="GB18030")
        name = soup.find('h1').contents[0]


        # 提取商品价格
        skuid = item['sku']
        price_url = 'http://p.3.cn/prices/get?type=1&skuid=J_'+skuid
        page = urllib.urlopen(urllib.unquote(price_url)).read()

        price = re.compile('\d*\.\d*').findall(page)[0]

        new_item = Item.objects.get_or_create(url=url)[0]
        new_item.name = name
        new_item.price = price
        new_item.img = img
        new_item.site = 'j'
        if new_item != None:
            print '一个野生的京东商品被加入了！'
        new_item.save()






