from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from shortener.forms import AuthForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'shortener.views.renderHome', name='home-url'),
    url(r'^about/$', 'shortener.views.renderHome', name='about-url'),
    url(r'^contact/$', 'shortener.views.renderHome', name='contact-url'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'authentication_form': AuthForm}, name="login-url"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout-url"),
    url(r'^_ajax/create-shortener/$', 'shortener.views.createBit', name='ajax-createbit-url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<bit>[\w_-]+)/$', 'shortener.views.renderBit'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media', 'show_indexes': True}),
    )

