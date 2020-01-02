from django.conf import settings
from django.db import models


# Create your models here.

class Stat(models.Model):
    url = models.URLField()

    query_selector = models.CharField(max_length=500)

    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="subscribed_stats")
