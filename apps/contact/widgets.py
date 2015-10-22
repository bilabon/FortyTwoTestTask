import os
from django.forms import DateInput
from django.contrib.admin.widgets import AdminFileWidget


class AdminImageWidget(AdminFileWidget):
    '''Override template for image widget'''

    template_with_initial = ('<div class="col-sm-2">Change:</div>'
                             '<div class="col-sm-10">%(input)s</div></br>')


class CalendarWidget(DateInput):

    def render(self, name, value, attrs=None):
        print 'attrs', attrs
        if not attrs:
            attrs = {'class': 'datewidget'}
        else:
            attrs['class'] = attrs.get('class', '') + ' datewidget'

        input_render = super(CalendarWidget, self).render(name, value, attrs)

        render = '''
            <div id="%(input_id)s" class="input-group date datetimepicker">
            %(input_render)s
            <span class="input-group-addon">
                <span class="glyphicon glyphicon-remove"></span></span>
            <span class="input-group-addon">
                <span class="glyphicon glyphicon-calendar"></span></span>
            </div>''' % {'input_render': input_render,
                         'input_id': attrs.get('id', '')}
        return render

    class Media:
        css = {
            'all': ('css/datetimepicker.css',)
        }
        js = ('js/bootstrap-datetimepicker.js', 'js/datetimepicker_init.js',)
