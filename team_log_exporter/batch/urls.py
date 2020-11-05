from django.urls import path

from . import views

urlpatterns = [
    # /batch
    path('', views.home, name='home'),
]