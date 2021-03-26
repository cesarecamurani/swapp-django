from django.conf import settings
from django.conf.urls.static import static

from swapp import views
from django.urls import path


urlpatterns = [
    path('', views.home.index, name='index'),
    path('register', views.authentication.register_request, name='register'),
    path('login', views.authentication.login_request, name='login'),
    path('logout', views.authentication.logout_request, name='logout'),
    path('users', views.users.users_request, name='users'),
    path('users/<str:username>/', views.users.user_request, name='user'),
    path('users/<str:username>/change_password', views.users.change_password_request, name='change_password'),
    path('users/<str:username>/swapp_requests/<str:trace_id>', views.users.swapp_request, name='swapp_request'),
    path('users/<str:username>/swapp_requests/<str:trace_id>/accept_swapp_request', views.users.accept_swapp_request, name='accept_swapp_request'),
    path('users/<str:username>/swapp_requests/<str:trace_id>/reject_swapp_request', views.users.reject_swapp_request, name='reject_swapp_request'),
    path('items/add_item', views.items.item_create_request, name='add_item'),
    path('items', views.items.items_request, name='items'),
    path('items/<uuid:item_id>/', views.items.item_request, name='item'),
    path('items/<uuid:item_id>/new_swapp_request', views.items.new_swapp_request, name='new_swapp_request'),
    path('items/<uuid:item_id>/delete', views.items.item_delete_request, name='delete'),
    path('donations', views.donations.donations_request, name='donations'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
