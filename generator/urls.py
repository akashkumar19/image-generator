from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_images, name='generate_images'),
]
