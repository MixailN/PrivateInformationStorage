from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<str:url_hash>', views.get_information),
]