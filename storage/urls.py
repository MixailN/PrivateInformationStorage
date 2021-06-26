from django.urls import path
from . import views
from .tasks import delete_expired_images

urlpatterns = [
    path('', views.index),
    path('storage/<str:url_hash>', views.get_information),
]


delete_expired_images()
