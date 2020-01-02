from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import TemplateView, CreateView
from paramiko import SSHClient, AutoAddPolicy

from Core.models import Stat


class DashboardView(TemplateView):
    template_name = "Dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["my_stats"] = self.request.user.subscribed_stats.all()

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

        command = "cd farid/selenium; python3.6 get_value.py '{}' '{}'".format(url, query_selector)

        print(command)

        client = SSHClient()

        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect('213.233.180.18', port=10147, username="amirhossein", password="frisbe")
        stdin, stdout, stderr = client.exec_command(command)

        value = stdout.read().decode('utf-8')[:-1]

        stat.last_value = value
        stat.save()

        return JsonResponse({"success": True, "value": value}, safe=False)


class AddStatView(TemplateView):
    template_name = "add-stat.html"

