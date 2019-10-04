from __future__ import unicode_literals

from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='rom/class/', blank=True, null=True, default=None)
    sort = models.IntegerField(default=0)