from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [path('', views.index, name="index"),
               path('demo/', views.show_form, name="processform"),
               path('templates/', views.show_templates, name="templates"),
               path('aboutus/', views.show_aboutus, name="aboutus"),
               path('contactus/', views.show_contactus, name="contactus"),
               path('startprocess/', views.initiate, name="initiate"),
               # default view call for this app
               ]
