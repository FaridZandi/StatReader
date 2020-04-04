from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import TemplateView, CreateView
from paramiko import SSHClient, AutoAddPolicy

from Core.models import Stat

from django.conf import settings


class DashboardView(TemplateView):
    template_name = "Dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # if self.request.is_authenticated():
        #     context["my_stats"] = self.request.user.subscribed_stats.all()
        # else:
        context["my_stats"] = Stat.objects.all()
        context["host_name"] = settings.HOST_URL

        return context


class StatAllView(View):
    def get(self, request):
        all_stat = Stat.objects.all()
        ids = []

        for stat in all_stat:
            ids.append(str(stat.id))

        return JsonResponse(",".join(ids), safe=False)


class StatUpdateView(View):
    def get(self, request):
        stat_id = int(self.request.GET.get("id"))

        stat = Stat.objects.get(id=stat_id)

        url = stat.url
        query_selector = stat.query_selector

        command = "cd farid/selenium; " \
                  "./kill-chrome.sh; " \
                  "python3.6 get_value.py '{}' '{}'; " \
                  "./kill-chrome.sh;".format(url, query_selector)

        client = SSHClient()

        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect('213.233.180.18',
                       port=10147,
                       username="amirhossein",
                       password="frisbe")

        stdin, stdout, stderr = client.exec_command(command)
        value = stdout.read().decode('utf-8')[:-1]

        stat.update_value(value)

        return JsonResponse({"success": True, "value": value}, safe=False)


class AddStatView(TemplateView):
    template_name = "add-stat.html"


class StatHistory(View):

    def get(self, request):
        stat_id = int(self.request.GET.get("id"))
        stat = Stat.objects.get(id=stat_id)

        histories = stat.stat_histories.all()[0:7]
        print(histories)

        result = {"id": stat_id,
                  "histories": [history.value for history in histories]}

        return JsonResponse(result)
