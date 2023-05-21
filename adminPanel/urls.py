from django.urls import path
from .import views

urlpatterns = [
    path('adminlogin/', views.adminLogin, name='adminLogin'),
    path('adminHome/', views.adminHome, name='adminHome'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('adminLogout/', views.adminLogout, name='adminLogout'),
]