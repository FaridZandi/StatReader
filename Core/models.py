from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.

class Stat(models.Model):
    name = models.CharField(max_length=50)

    url = models.URLField()

    query_selector = models.CharField(max_length=500)

    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="subscribed_stats")

    last_value = models.CharField(max_length=20)

    last_updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Stat, self).save(*args, **kwargs)

