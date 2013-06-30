# coding: utf8


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from PriceCompare.models import Item
from PriceCompare.forms import MyUserCreationForm

import hashlib

def home(request):
    '''
    访问主页 （处理搜索请求）
    '''

    query = ''
    if 'q' in request.GET:
        query = request.GET['q']

    return render_to_response('home.html', {
        'request': request,
        'query': query,
    }, context_instance=RequestContext(request))


def register(request):
    '''
    处理新用户注册，成功后自动跳转
    '''

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('home', ))
    else:
        form = MyUserCreationForm()
    return render_to_response("register.html", {
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def manage(request):
    '''
    用户个人中心
    '''
    return render_to_response('manage.html', {
        'request': request,
    }, context_instance=RequestContext(request))