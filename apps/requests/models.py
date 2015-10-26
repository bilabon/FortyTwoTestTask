from django.db import models


class RequestLog(models.Model):
    """
    Model for saving request data to database
    """
    method = models.CharField(max_length=10)
    path_info = models.CharField(max_length=200)
    server_protocol = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return "Request {0} {1} {2}".format(
            self.method, self.path_info, self.server_protocol)
