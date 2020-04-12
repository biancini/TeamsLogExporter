from django.urls import path

from . import views

urlpatterns = [
    # /exporter
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),
    path('bearer', views.bearer, name='bearer'),
    path('getusers_bygroup', views.getusers_bygroup, name='getusers_bygroup'),
    path('getuser_meetings', views.getuser_meetings, name='getuser_meetings'),
    path('getmeeting_records', views.getmeeting_records, name='getmeeting_records'),
    path('', views.home, name='home'),
]