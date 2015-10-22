import os
from django.contrib.admin.widgets import AdminFileWidget


class AdminImageWidget(AdminFileWidget):
    '''Override template for image widget'''

    template_with_initial = ('<div class="col-sm-2">Change:</div>'
                             '<div class="col-sm-10">%(input)s</div></br>')
