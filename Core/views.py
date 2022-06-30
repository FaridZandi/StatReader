import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView
from paramiko import SSHClient, AutoAddPolicy
from Core.models import Stat, StatHistoryDaily, StatHistoryHourly
from django.conf import settings


class DashboardView(TemplateView):
    template_name = "Dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # if self.request.is_authenticated():
        #     context["my_stats"] = self.request.user.subscribed_stats.all()
        # else:
        context["my_stats"] = Stat.objects.all()
        context["host_url"] = settings.HOST_URL

        return context


class StatAllView(View):
    def get(self, request):
        result = []
        for stat in Stat.objects.all():
            result.append({
                "id": stat.id,
                "url": stat.url,
                "query_selector": stat.query_selector
            })
        return JsonResponse(result, safe=False)


class StatUpdateView(View):
    @csrf_exempt
    def post(self, request):
        data = request.POST
        if "password" not in data or data["password"] != "masalansecure":
            return JsonResponse({"success": False})

        if "id" not in data or "value" not in data:
            return JsonResponse({"success": False})
        print(int(data["id"]))

        stat = Stat.objects.get(id=int(data["id"]))
        value = data["value"]

        stat.update_value(value)
        return JsonResponse({"success": True})


    def get(self, request):
        stat_id = int(self.request.GET.get("id"))

        stat = Stat.objects.get(id=stat_id)

        uid = stat.id
        url = stat.url
        query_selector = stat.query_selector

        command = "cd crawler; " \
                  "python3 get_value.py '{}' '{}' {};".format(url, query_selector, uid)

        step_1_command = "ssh sim-02 \"{}\"".format(command) 


        client = SSHClient()

        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect('syslab.cs.toronto.edu',
                       port=22,
                       username="faridzandi",
                       password="applebanana456")

        stdin, stdout, stderr = client.exec_command(step_1_command)

        value = stdout.read().decode('utf-8')[:-1]
        print(value) 

        # stat.update_value(value)

        return JsonResponse({"success": True, "value": value}, safe=False)


class AddStatView(TemplateView):
    template_name = "add-stat.html"


class StatHistory(View):
    def get(self, request):
        stat_id = int(self.request.GET.get("id"))
        stat = Stat.objects.get(id=stat_id)

        result = {
            "id": stat_id,
            "histories_daily": StatHistoryDaily.get_values(stat),
            "histories_hourly": StatHistoryHourly.get_values(stat)
        }

        return JsonResponse(result)
