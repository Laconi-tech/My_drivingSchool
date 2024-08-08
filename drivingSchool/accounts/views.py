from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

def login_user(request):
    if request.method == "POST":
        username_user = request.POST["username"]
        password_user = request.POST["password"]

        user = authenticate(request, username = username_user, password = password_user)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")
    
    form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect('index')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
             # Ajout de l'utilisateur au groupe par défaut
            default_group, created = Group.objects.get_or_create(name='student')
            user.groups.add(default_group)
            return redirect("index")
    else:
        form = UserCreationForm()
    
    return render(request, "accounts/register.html", {"form": form})