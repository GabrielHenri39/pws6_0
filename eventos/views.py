from django.shortcuts import render,redirect, get_object_or_404
from .models import Evento
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.


@login_required
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')

        logo = request.FILES.get('logo')

        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )

        evento.save()

        messages.add_message(request, constants.SUCCESS,
                             'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))

@login_required
def gerenciar_evento(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)
        if nome:
            eventos = eventos.filter(nome__contains=nome)

        return render(request, 'gerenciar_evento.html', {'eventos': eventos})

@login_required
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == "GET":
        return render(request, 'inscrever_evento.html', {'evento': evento})
    elif request.method == "POST":
        if request.user in evento.participantes.all() or request.user == evento.criador:
            messages.add_message(request, constants.WARNING, 'você já está inscrito ou você e criador')
            return redirect(reverse('inscrever_evento', kwargs={'id': id}))
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, constants.SUCCESS, 'Inscrição com sucesso.')
        return redirect(reverse('inscrever_evento', kwargs={'id': id}))

def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == "GET":
        participantes = evento.participantes.all()[::3]
        return render(request, 'participantes_evento.html', {'evento': evento, 'participantes': participantes})