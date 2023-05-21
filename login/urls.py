from django.urls import path
from .import views

urlpatterns = [
    path("", views.index,name ='login'),  
    path("signup", views.signup,name ='signup'), 
    path("user_homepage", views.user_homepage,name ='user_homepage'), 
    path("sign_out/", views.sign_out,name ='sign_out'), 
]