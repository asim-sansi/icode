from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [path('', views.index, name="index"),
               path('startprocess/', views.initiate, name="initiate"),
               # default view call for this app
               ]
