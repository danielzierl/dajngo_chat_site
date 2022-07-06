from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('<int:pk>', views.detail, name='detail'),
    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<int:pk>', views.updateRoom, name='update_room'),
    path('delete-room/<int:pk>', views.deleteRoom, name='delete_room'),
    path('delete-message/<int:pk>', views.deleteMessage, name='delete_message'),
    path('userProfile/<int:pk>', views.userProfile, name='user_profile')
]
