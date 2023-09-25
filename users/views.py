from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from .forms import LoginForm

def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Credentials")
                return redirect("login")
    context = {'form': forms}
    return render(request, 'users/login.html', context)



def logout_page(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name,email=email,password=password,username = username )
            user.save()

            return redirect('login')       
    else:
        form = RegistrationForm()
    context={
        'form': form,
    }
    return render(request, "users/register.html", context=context)
