from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from .models import Student
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from login import views

# Create your views here.

@never_cache
def adminLogin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(adminHome)
    if request.user.is_authenticated:
        return redirect(views.index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                username = user.username
                return redirect(adminHome)
            else:
                messages.error(request, "You are not authorized to access this webpage!!!")
                return redirect(adminLogin)
        else:
            messages.error(request, 'Username or Password is wrong!')
            return redirect(adminLogin)
    return render(request, 'adminLogin.html')


@never_cache
def adminHome(request):
    if request.user.is_authenticated and request.user.is_superuser:
        students = User.objects.all()
        if request.method == 'GET'and request.GET.get('search') is not None:
            print(request.GET)
            students = User.objects.annotate(search=SearchVector('username','email')).filter(search=request.GET.get('search'))
            return render(request, 'adminHome.html',{'students':students})

        return render(request, 'adminHome.html',{'students':students})
    return redirect(adminLogin)

def add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect(add)

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect(add)
        
            if len(username)>10:
                messages.error(request, "Username must be under 10 charcters!!")
                return redirect(add)
        
            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect(add)
        
            myuser = User.objects.create_user(username,email,pass1)
            myuser.save()
            messages.success(request, "Your Account has been successfully created!")
            return redirect(adminHome)
    
        return render(request,'add.html')
    
    return redirect(adminLogin)

def edit(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            User.objects.filter(id=id).update(username=username,email=email)
        else:
            data = User.objects.get(id=id)
            return render(request, 'edit.html',{'student':data})
    messages.success(request, "Details have been Updated")
    return redirect(adminLogin)


def delete(request,id):
    if request.user.is_authenticated:
        student = User.objects.get(id=id)
        student.delete()
        messages.success(request, "Deleted a record successfully.")
        return redirect(adminHome)
    return redirect(adminHome)


def adminLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged Out Successfully')
        return redirect(adminLogin)
    
