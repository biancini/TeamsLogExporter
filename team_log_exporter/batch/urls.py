from django.urls import path

from . import views

urlpatterns = [
    # /batch
    path('', views.home, name='home'),
    path('upload_csvfile', views.upload_csvfile, name='upload_csvfile'),
]