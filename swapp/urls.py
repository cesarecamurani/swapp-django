from django.urls import path, include

from . import views


urlpatterns = (
    path('', views.home.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', views.authentication.register_request, name='register'),
    path('login', views.authentication.login_request, name='login'),
    path('logout', views.authentication.logout_request, name='logout'),
)
