from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def admin_url(obj):
    '''
    Tag that accepts any object and renders the link to its admin edit page
    '''
    if obj:
        url = reverse('admin:{0}_{1}_change'.format(
            obj._meta.app_label, obj._meta.module_name), args=[obj.pk])

        html = '<a href="%s">(Admin)</a>' % url
        return mark_safe(html)
