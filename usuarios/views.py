from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from .utils import password_is_valid
from django.contrib import messages
from django.contrib.messages import constants



def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not password_is_valid(request=request,password=senha, confirm_password= confirmar_senha):
            return redirect(reverse('cadastro'))

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
            return redirect(reverse('cadastro'))

        user = User.objects.create_user(
            username=username, email=email, password=senha)
        user.save()
        return redirect(reverse('login'))


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect(reverse('login'))
        
        auth.login(request, user)
        return redirect('/eventos/novo_evento/')


def sair(request):
    auth.logout(request)
    return redirect(reverse('login'))