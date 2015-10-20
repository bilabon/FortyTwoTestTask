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
