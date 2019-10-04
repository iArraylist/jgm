from __future__ import unicode_literals

from django.db import models


class Member(models.Model):
    user = models.ForeignKey('auth.User')
    facebook_id = models.BigIntegerField(db_index=True)
    facebook_token = models.CharField(max_length=1024)
    email = models.EmailField()
    username = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)