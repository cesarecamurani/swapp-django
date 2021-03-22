from swapp import views
from django.urls import path


urlpatterns = (
    path('', views.home.index, name='index'),
    path('register', views.authentication.register_request, name='register'),
    path('login', views.authentication.login_request, name='login'),
    path('logout', views.authentication.logout_request, name='logout'),
    path('users', views.users.users_request, name='users'),
    path('users/<str:username>/', views.users.user_request, name='user'),
    path('items/add_item', views.items.item_create_request, name='add_item'),
    path('items', views.items.items_request, name='items'),
    path('items/<int:item_id>/', views.items.item_request, name='item'),
    path('items/<uuid:item_id>/delete', views.items.item_delete_request, name='delete'),
    path('donations', views.donations.donations_request, name='donations'),
)
