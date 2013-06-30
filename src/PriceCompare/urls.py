from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'PriceCompare.views.home', name='home'),

    # user session

    url(r'^register/$', 'PriceCompare.views.register', name='register'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name=

'login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name=

'logout'),

    # user management
    url(r'^manage/$', 'PriceCompare.views.manage', name='manage'),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # ajax
    url(r'^ajax/user/$', 'PriceCompare.ajax.user', name='ajax_user'),
    url(r'^ajax/items/$', 'PriceCompare.ajax.items', name='ajax_items'),

    url(r'^ajax/favorite/$', 'PriceCompare.ajax.favorite', name='ajax_favorite'),
    # search
    url(r'^ajax/search/$', 'PriceCompare.ajax.search', name='ajax_search'),
)
