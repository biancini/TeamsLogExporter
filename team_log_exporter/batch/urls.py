from django.urls import path
from . import views

urlpatterns = [
    # /batch
    path('signin', views.sign_in, name='batch_signin'),
    path('signout', views.sign_out, name='batch_signout'),
    path('callback', views.callback, name='batch_callback'),
    path('bearer', views.bearer, name='batch_bearer'),
    path('', views.home, name='batch_home'),
    path('upload_csvfile', views.upload_csvfile, name='upload_csvfile'),
    path('download_jsonapi', views.download_jsonapi, name='download_jsonapi'),
    path('generate_excel', views.generate_excel, name='generate_excel'),
]