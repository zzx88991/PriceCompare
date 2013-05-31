from django.conf.urls import patterns, url

urlpatterns = patterns('',

		url(r'^$', 'PriceCompare.views.index', name='index'),

		url(r'^register/?$', 'PriceCompare.views.register', name='register'),

		)
