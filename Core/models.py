from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.

class Stat(models.Model):
    created = models.DateTimeField(default=timezone.now,
                                   editable=False)

    modified = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=50)

    url = models.URLField()

    query_selector = models.CharField(max_length=500)

    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True, blank=True)

    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="subscribed_stats",
                                         null=True, blank=True)

    last_value = models.CharField(max_length=20,
                                  default="0")

    last_updated = models.DateTimeField(default=timezone.now)

    prefix = models.CharField(max_length=5, null=True, blank=True)

    suffix = models.CharField(max_length=5, null=True, blank=True)

    @property
    def get_subscribers_count(self):
        return self.subscribers.count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Stat, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-name',)

