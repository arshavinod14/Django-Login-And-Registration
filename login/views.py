from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from adminPanel.views import adminHome

# Create your views here.

def index(request):
    if request.user.is_authenticated and request.user.is_superuser :
        #print(request.user)
        return redirect(adminHome)
    
    if request.user.is_authenticated:
        print(request.user)
        return redirect(user_homepage)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_superuser:
                messages.error(request, "You are not authorized to access this webpage!!!")
                return render(request, 'login.html')

            login(request, user)
            return render(request,'user_homepage.html',{'username':request.user.username})
        else:
            messages.error(request, 'Username or Password is wrong!')
            return render(request, 'login.html')
    else:
        print("Wrong!!!!!!!!!!")
        return render(request, 'login.html')
        
    #     def index(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']

    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         if user.is_superuser:
    #             login(request, user)
    #             return redirect(adminHome)
    #         else:
    #             messages.error(request, "You are not authorized to access this webpage!!!")
    #             return render(request, 'login.html')
    #     else:
    #         messages.error(request, 'Username or Password is wrong!')
    #         return render(request, 'login.html')
    # else:
    #     if request.user.is_authenticated:
    #         if request.user.is_superuser:
    #             return redirect(adminHome)
    #         return redirect(user_homepage)
    #     return render(request, 'login.html')

            

def signup(request):
    if request.user.is_authenticated:
        return redirect(adminHome)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

    # return render(request,'register.html')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect(signup)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect(signup)
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 charcters!!")
            return redirect(signup)
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect(signup)
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()

        messages.success(request, "Your Account has been successfully created!")
        return redirect(index)
        #return render(request, 'login.html')
    
    return render(request,'register.html')


def user_homepage(request):
    if request.user.is_authenticated and not request.user.is_superuser :
        print("Logged")
        return render(request,"user_homepage.html")
    else:
        return redirect(index)


def sign_out(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        logout(request)
        print("LoggedOut")
        messages.success(request, 'Logged Out Successfully')
        return redirect(index)
