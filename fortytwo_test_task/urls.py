from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.contact.views import HomeView, RequestLogListView, RequestCountView


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^request-log/$', RequestLogListView.as_view(), name='request-log'),
    url(r'^request-count/$', RequestCountView.as_view(), name='request-count'),
)
