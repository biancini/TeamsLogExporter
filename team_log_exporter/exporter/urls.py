from django.urls import path

from . import views

urlpatterns = [
    # /exporter
    path('signin', views.sign_in, name='exporter_signin'),
    path('signout', views.sign_out, name='exporter_signout'),
    path('callback', views.callback, name='exporter_callback'),
    path('bearer', views.bearer, name='exporter_bearer'),
    path('getusers_bygroup', views.getusers_bygroup, name='getusers_bygroup'),
    path('getuser_meetings', views.getuser_meetings, name='getuser_meetings'),
    path('getmeeting_records', views.getmeeting_records, name='getmeeting_records'),
    path('export_xls', views.export_xls, name='export_xls'),
    path('', views.home, name='exporter_home'),
]