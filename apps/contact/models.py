from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    """
    Extending the User model with additional fields
    """
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contacts = models.TextField()

    def __unicode__(self):
        return self.user


class RequestLog(models.Model):
    """
    Model for saving all http requests to database
    """
    http_request = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return self.request
