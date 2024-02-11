"""ebdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
        path('admin/', admin.site.urls),
	path('home/', views.pylinkweb),
        path('real/', views.realweb),#新增這一列
        path('fv/', views.deposits),  #新增這一列
        path('result/', views.result),
        path('realresult/', views.realresult),
        path('postreal/', views.postreal),
        path('realstop/', views.realstop),
]
