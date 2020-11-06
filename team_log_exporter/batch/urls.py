from django.urls import path

from . import views

urlpatterns = [
    # /batch
    path('', views.home, name='home'),
    path('upload_csvfile', views.upload_csvfile, name='upload_csvfile'),
    path('download_json', views.download_json, name='download_json'),
    path('download_jsonzip', views.download_jsonzip, name='download_jsonzip'),
]