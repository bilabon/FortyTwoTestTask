from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contacts = models.TextField()

    def __unicode__(self):
        return self.name
