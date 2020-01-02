from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views import View
import subprocess
import sys

from paramiko import SSHClient, AutoAddPolicy


class TestView(View):

    def get(self, request, *args, **kwargs):
        command = "cd farid/seleniumtest; python3.6 test.py"
        client = SSHClient()

        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect('213.233.180.18', port=10147, username="amirhossein", password="frisbe")
        stdin, stdout, stderr = client.exec_command(command)
        return HttpResponse(stdout)
