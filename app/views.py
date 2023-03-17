from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, optform
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Contact

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "There was a problem logging in. Try again ...")
            return redirect('home')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})



class HomeListView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = Contact
    context_object_name = "contacts"

    def get_queryset(self):
        contacts = super().get_queryset()
        return contacts.filter(manager=self.request.user)

def form(request):
    form = optform()
    if request.method == 'POST':
        form = optform(request.POST)
        if form.is_valid():
            form.save()
            form = optform()
            return redirect('home')
    return render(request, 'form.html', {'form':form})