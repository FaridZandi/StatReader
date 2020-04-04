"""StatReader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

from django.urls import path, include, re_path
from Core.views import DashboardView, AddStatView, StatAllView, StatUpdateView, StatHistory

# import Core.views

urlpatterns = [

    path('',
         RedirectView.as_view(url="dashboard/", permanent=False),
         name="root"),

    path('dashboard/',
         DashboardView.as_view(),
         name="dashboard"),

    path('stat/all/',
         StatAllView.as_view(),
         name="stat-all"),

    path('stat/update/',
         StatUpdateView.as_view(),
         name="stat-update"),

    path('stat/add/',
         AddStatView.as_view(),
         name="add-stat"),

    path('stat/history/',
         StatHistory.as_view(),
         name="stat-history"),
]
