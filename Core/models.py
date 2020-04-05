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
                                         blank=True)

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

        StatHistoryDaily.update_history(self, value)
        StatHistoryHourly.update_history(self, value)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Stat, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


class StatHistoryHourly(models.Model):
    stat = models.ForeignKey(to=Stat,
                             related_name="stat_histories_hourly",
                             verbose_name="stat",
                             on_delete=models.CASCADE)

    value = models.CharField(verbose_name="value",
                             max_length=20,
                             default="0")

    hour = models.DateTimeField()

    @staticmethod
    def get_values(stat):
        histories_hourly_values = []

        one_day = timezone.timedelta(days=1)
        yesterday = timezone.now() - one_day
        histories_hourly = stat.stat_histories_hourly.order_by('hour').filter(
            hour__gt=yesterday
        )

        if len(histories_hourly) == 0:
            return histories_hourly_values

        one_hour = timezone.timedelta(hours=1)
        first_hour = histories_hourly[0].hour
        last_hour = histories_hourly[len(histories_hourly) - 1].hour

        current_hour = first_hour
        histories_index = 0
        while current_hour <= last_hour:
            h = histories_hourly[histories_index]
            if current_hour == h.hour:
                value = ''.join(c for c in h.value if c.isdigit() or c == '.')
                if len(value) == 0:
                    value = None
                histories_hourly_values.append(value)
                histories_index += 1
            else:
                histories_hourly_values.append(None)
            current_hour += one_hour

        return histories_hourly_values

    @staticmethod
    def update_history(stat, value):
        current_hour = timezone.now()
        current_hour = current_hour.replace(minute=0, second=0, microsecond=0)

        histories = StatHistoryHourly.objects.filter(hour=current_hour,
                                                     stat__id=stat.id).all()

        if len(histories) == 0:
            StatHistoryHourly.objects.create(stat=stat,
                                             hour=current_hour,
                                             value=value)

            histories_count = stat.stat_histories_hourly.count()

            history_count_keep = 24
            if histories_count > history_count_keep:
                delete_count = histories_count - history_count_keep
                deleted = stat.stat_histories_hourly.order_by("hour")[:delete_count]
                for d in deleted:
                    d.delete()
        else:
            hist = histories[0]
            hist.value = value
            hist.save()

    class Meta:
        verbose_name = "Stat History (Hourly)"
        verbose_name_plural = "Stat History (Hourly)"


class StatHistoryDaily(models.Model):
    stat = models.ForeignKey(to=Stat,
                             related_name="stat_histories_daily",
                             verbose_name="stat",
                             on_delete=models.CASCADE)

    value = models.CharField(verbose_name="value",
                             max_length=20,
                             default="0")

    date = models.DateField()

    @staticmethod
    def get_values(stat):
        histories_daily_values = []

        thirty_days = timezone.timedelta(days=30)
        month_ago = (timezone.now() - thirty_days).date()
        histories_daily = stat.stat_histories_daily.order_by('date').filter(
            date__gt=month_ago
        )

        if len(histories_daily) == 0:
            return histories_daily_values

        one_day = timezone.timedelta(days=1)
        first_day = histories_daily[0].date
        last_day = histories_daily[len(histories_daily) - 1].date

        current_day = first_day
        histories_index = 0
        while current_day <= last_day:
            h = histories_daily[histories_index]
            if current_day == h.date:
                value = ''.join(c for c in h.value if c.isdigit() or c == '.')
                if len(value) == 0:
                    value = None
                histories_daily_values.append(value)
                histories_index += 1
            else:
                histories_daily_values.append(None)
            current_day += one_day

        return histories_daily_values

    @staticmethod
    def update_history(stat, value):
        current_date = timezone.now().date()

        histories = StatHistoryDaily.objects.filter(stat__id=stat.id,
                                                    date=current_date).all()

        if len(histories) == 0:
            StatHistoryDaily.objects.create(stat=stat,
                                            date=current_date,
                                            value=value)

            histories_count = stat.stat_histories_daily.count()

            history_count_keep = 30
            if histories_count > history_count_keep:
                delete_count = histories_count - history_count_keep
                deleted = stat.stat_histories_daily.order_by("date")[:delete_count]
                for d in deleted:
                    d.delete()
        else:
            hist = histories[0]
            hist.value = value
            hist.save()

    class Meta:
        verbose_name = "Stat History (Daily)"
        verbose_name_plural = "Stat History (Daily)"
