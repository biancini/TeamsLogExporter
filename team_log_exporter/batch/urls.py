from django.urls import path
from . import views

urlpatterns = [
    # /batch
    path('', views.home, name='home'),
    path('upload_csvfile', views.upload_csvfile, name='upload_csvfile'),
    path('download_jsonapi', views.download_jsonapi, name='download_jsonapi'),
    path('generate_excel', views.generate_excel, name='generate_excel'),
]