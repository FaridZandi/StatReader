from django.contrib import admin
from Core.models import Stat


# Register your models here.

class StatAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "query_selector", "creator")

    class Meta:
        model = Stat

admin.site.register(Stat, StatAdmin)

