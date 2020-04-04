from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date


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

    def update_value(self, value):
        self.last_value = value
        self.save()

        current_date = timezone.now().date()

        histories = StatHistoryDaily.objects.filter(stat__id=self.id,
                                                    date=current_date).all()

        print(histories)
        print(len(histories))

        if len(histories) == 0:
            StatHistoryDaily.objects.create(stat=self,
                                            date=current_date,
                                            value=value)

            histories_count = self.stat_histories.count()

            history_count_keep = 30
            if histories_count > history_count_keep:
                delete_count = histories_count - history_count_keep
                deleted = self.stat_histories.order_by("date")[:delete_count]
                for d in deleted:
                    d.delete()
        else:
            hist = histories[0]
            hist.value = value
            hist.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Stat, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " currently at " + self.last_value

    class Meta:
        ordering = ('-name',)


class StatHistoryDaily(models.Model):
    stat = models.ForeignKey(to=Stat,
                             related_name="stat_histories",
                             verbose_name="stat",
                             on_delete=models.CASCADE)

    value = models.CharField(verbose_name="value",
                             max_length=20,
                             default="0")

    date = models.DateField()

    class Meta:
        verbose_name = "Stat History"
        verbose_name_plural = "Stat History (Daily)"
