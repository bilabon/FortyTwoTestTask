from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Contact(models.Model):
    """
    Extending the User model with additional fields
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    contacts = models.TextField(max_length=500, blank=True)
    email = models.EmailField(blank=True)
    jabber = models.EmailField(blank=True)
    skype = models.CharField(max_length=30, blank=True)

    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(200, 200)],
                                      format='PNG',
                                      options={'quality': 60})

    def __unicode__(self):
        return "{0} {1} {2}".format(self.id, self.first_name, self.last_name)
