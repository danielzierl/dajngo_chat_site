from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>', views.detail, name='detail'),
    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<int:pk>', views.updateRoom, name='update_room'),
    path('delete-room/<int:pk>', views.deleteRoom, name='delete_room'),
]
