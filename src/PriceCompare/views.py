import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from PriceCompare.models import User

def index(request):

	context = {}
	return render(request, 'index.html', context)

def register(request):

	context = {}
	return render(request, 'register.html', context)
