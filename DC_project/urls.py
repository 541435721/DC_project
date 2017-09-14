"""DC_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from DC import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home_page'),
    url(r'^regist/', views.regist, name='register'),
    url(r'^login/', views.login, name='login'),
    # url(r'^write/', views.write_DB, name='write'),
    url(r'^user/', views.user, name='user_center'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^basic_table/', views.basic_table, name='basic_table'),
    url(r'^complete_table/', views.complete_table, name='complete_table'),
    url(r'^line_chart/', views.line_chart, name='line_chart'),
    url(r'^columnar_chart/', views.columnar_chart, name='columnar_chart'),
    url(r'^pie_chart/', views.pie_chart, name='pie_chart'),

]
