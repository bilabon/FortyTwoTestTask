from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from apps.contact.views import HomeView, AjaxContactEditView
from apps.requests.views import (RequestLogListView, RequestCountView, )


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'auth/login.html',
    }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'template_name': 'auth/logout.html',
        'next_page': '/',
    }, name='logout'),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^requests/$', RequestLogListView.as_view(), name='request-log'),
    url(r'^request-count/$', RequestCountView.as_view(), name='request-count'),

    url(r'^edit/$', login_required(AjaxContactEditView.as_view()),
        name='ajax_contact_edit_view'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
