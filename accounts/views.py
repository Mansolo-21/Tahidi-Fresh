from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegisterForm,LoginForm
from .models import User
from django.shortcuts import redirect


# Create your views here.
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"])
            
            messages.success(request,"Account Successfully Created"
                             )
        return redirect("login")
    
    return render(request,"accounts/register.html",{"form":form})

def login_view(request):
    form = LoginForm()
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )
            if user is not None:
                login(request, user)
            if user.role == "shopper":
                return redirect("shopper_dashboard")
            elif user.role == "rider":
                return redirect("rider_dashboard")
            elif user.role == "admin":
                return redirect("owner_dashboard")
            return redirect("dashboard")
            
            
    return render(request,"accounts/login.html",{"form":form})



def logout_view(request):
    logout(request)
    return redirect('login')  # replace with your login URL name