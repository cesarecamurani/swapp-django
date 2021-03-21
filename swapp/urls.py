from swapp import views
from django.urls import path


urlpatterns = (
    path('', views.home.index, name='index'),
    path('register', views.authentication.register_request, name='register'),
    path('login', views.authentication.login_request, name='login'),
    path('logout', views.authentication.logout_request, name='logout'),
    path('users', views.users.users_request, name='users'),
    path('users/<str:username>/', views.users.user_request, name='user'),
)
