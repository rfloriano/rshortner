from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'shorter.views.renderHome', name='home-url'),
    url(r'^about/$', 'shorter.views.renderHome', name='about-url'),
    url(r'^contact/$', 'shorter.views.renderHome', name='contact-url'),
    url(r'^_ajax/create-shortener/$', 'shorter.views.createBit', name='ajax-createbit-url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<bit>[\w_-]+)/$', 'shorter.views.renderBit'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media', 'show_indexes': True}),
    )

