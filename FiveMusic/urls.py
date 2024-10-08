"""FiveMusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from coze_app import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', views.index, name='index'),
    path('paint/', views.paint, name='paint'),
    path('loading/', views.loading, name='loading'),

    path('htp/', views.htp, name='htp'),
    path('htp_view/', views.htp_view, name='htp_view'),

    path('flower/', views.flower, name='flower'),
    path('bigscreen/', views.bigscreen, name='bigscreen'),

    path('aitalk/', views.aitalk, name='aitalk'),
    path('aitalk_res/', views.get_coze_suggest, name='get_coze_suggest'),

    path('check_status/', views.check_status, name='check_status')
]
