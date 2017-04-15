"""blockchain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),

    # user manage
    url(r'^userhandle$', views.userhandle, name='userhandle'),
    url(r'^userdelete$', views.userdelete, name='userdelete'),
    url(r'^useradd$', views.useradd, name='useradd'),
    url(r'^modifyauth$', views.modifyauth, name='modifyauth'),

    # host manage
    url(r'^hostquery$', views.hostquery, name='hostquery'),
    url(r'^hostdelete$', views.hostdelete, name='hostdelete'),
    url(r'^hostadd$', views.hostadd, name='hostadd'),
    url(r'^hostmodify$', views.hostmodify, name='hostmodify'),

    # build network
    url(r'^build$', views.build, name='build'),

    # blockchain information visual
    url(r'^show$', views.show, name='show'),
    url(r'^new_block$', views.new_block, name='new_block'),
    url(r'^visual$', views.visual, name='visual'), # debug
    url(r'^addBlock$', views.add_new_block, name='addBlock'), # debug

    # auth manage
    url(r'^admin/', admin.site.urls),
]
