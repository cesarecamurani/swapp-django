from django.urls import path

from . import views

urlpatterns = (
    path('', views.home.index, name='index'),
    path('register', views.authentication.register, name='register')
)
