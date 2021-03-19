from django.urls import path, include

from . import views

urlpatterns = (
    path('', views.home.index, name='index'),
    path('register', views.authentication.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls'))
)
