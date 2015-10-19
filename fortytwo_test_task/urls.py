from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from apps.contact.views import HomeView


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
)
