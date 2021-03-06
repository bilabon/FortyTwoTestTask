import json
from django.http import HttpResponse


def render_to_json_response(context, **response_kwargs):
    '''
    returns a JSON response, transforming 'context' to make the payload
    '''
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(convert_context_to_json(context), **response_kwargs)


def convert_context_to_json(context):
    # convert the context dictionary into a JSON object
    # note: this is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects -- such as Django model instances or querysets
    # -- can be serialized as JSON.
    return json.dumps(context)


class AjaxFormResponseMixin(object):
    '''
    A mixin to add AJAX support to a form,
    must be used with an object-based FormView (e.g. CreateView)
    '''

    def form_invalid(self, form):
        return render_to_json_response(form.errors, status=400)

    def form_valid(self, form):

        # save
        self.object = form.save()

        # initialize a context with responce
        avatar_thumbnail = None
        if self.object.avatar_thumbnail:
            avatar_thumbnail = self.object.avatar_thumbnail.url

        context = {'success': True,
                   'AjaxFormResponseMixin': True,
                   'avatar_thumbnail': avatar_thumbnail, }
        # return the context as json
        return render_to_json_response(context)
