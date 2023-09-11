from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('create-room/', views.createRoom, name="Create-Room"),
    path('update-room/<str:pk>/', views.updateRoom, name="Update-Room"),
    path('delete/<str:pk>/', views.deleteRoom, name="Delete"),
]
