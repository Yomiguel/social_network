from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="Login"),
    path('logout/', views.logoutUser, name="Logout"),
    path('register/', views.registerPage, name="Register"),
    path('', views.home, name="Home"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('create-room/', views.createRoom, name="Create-Room"),
    path('update-room/<str:pk>/', views.updateRoom, name="Update-Room"),
    path('delete/<str:pk>/', views.deleteRoom, name="Delete"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="Delete-Comment"),
    path('user-profile/<str:pk>/', views.userProfile, name="User-Profile"),
]
