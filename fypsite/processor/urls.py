from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [path('', views.index, name="index"),
               path('demo/', views.show_form, name="processform"),
               path('templates/', views.show_templates, name="templates"),
               path('aboutus/', views.show_aboutus, name="aboutus"),
               path('contactus/', views.show_contactus, name="contactus"),
               path('demo/startprocess/', views.initiate, name="initiate"),
               path('demo/trackprocess/', views.trackProcess, name="track"),
               path('demo/viewpage/', views.viewPage, name="viewpage"),
               path('demo/viewcode/', views.viewCode, name="viewcode"),
               path('demo/download/', views.download, name="download"),
               # default view call for this app
               ]
