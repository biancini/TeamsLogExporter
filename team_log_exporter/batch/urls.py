from django.urls import path

from . import views

urlpatterns = [
    # /batch
    path('', views.home, name='home'),
    path('upload_csvfile', views.upload_csvfile, name='upload_csvfile'),
    path('download_jsonapi', views.download_jsonapi, name='download_jsonapi'),
    path('download_json', views.download_json, name='download_json'),
    path('download_jsonzip', views.download_jsonzip, name='download_jsonzip'),
    path('generate_excel', views.generate_excel, name='generate_excel'),
    path('download_excel', views.download_excel, name='download_excel'),
    path('download_excelzip', views.download_excelzip, name='download_excelzip'),
]