from django.shortcuts import render, redirect
from .models import RNA, Neuronio, Erro
import datetime
import json
import numpy as np
import random


def hello_msg():
    hour = datetime.datetime.now().strftime('%H')
    hour = int(hour)
    if hour >= 0 and hour <= 11:
        message = "Bom Dia!"
    elif hour >= 12 and hour <= 17:
        message = "Boa Tarde!"
    else:
        message = "Boa Noite!"

    return message


def str2bool(v):
    if v is None:
        return False
    return v.lower() in ("true", )


def home(request):
    message = hello_msg()

    if request.method == 'GET':
        return render(request, 'app/home.html', {'message': message})
    if request.method == 'POST':
        return redirect('perguntas')


def perguntas(request):
    error = False
    if request.method == 'POST':
        return redirect('resultados')
    return render(request, 'app/perguntas.html', {'error': error})


def resultados(request):
    RNA.objects.all().delete()
    for n in range(30):
         r = RNA()
         r.name = "Produto " + str(n)
         r.price = random.randint(1,30)
         r.save()

    queryset = RNA.objects.all()
    names = [obj.name for obj in queryset]
    prices = [int(obj.price) for obj in queryset]
    x = np.random.rand(5)
    y = np.random.rand(5)
    index = [i for i in range(5)]

    context = {
        'names': json.dumps(names),
        'prices': json.dumps(prices),
        'x': json.dumps(x.tolist()),
        'y': json.dumps(y.tolist()),
        'index': json.dumps(index),
    }
    return render(request, 'app/resultados.html', context)


def configuracoes(request):
    if request.method == 'GET':
        rna = RNA.objects.get_or_create(pk=1)[0]
        context = {
            'bias': rna.bias,
            'ft': rna.funcao_transferencia,
            'inter': rna.intervalo,
        }
        return render(request, 'app/configuracoes.html', context)
    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('home')
        else:
            if 'submit-conf' in request.POST:
                #update configs
                neuronios = Neuronio.objects.all().delete()
                rna = RNA.objects.get_or_create(id=1)[0]
                rna.bias = str2bool(request.POST.get("bias"))
                rna.funcao_transferencia = request.POST.get("ft")
                rna.intervalo = request.POST.get("inter")
                rna.save()
            if 'submit-train' in request.POST:
                #update no valor da epoca, usando abs()
                #executar funcao de treino
                rna = RNA.objects.get_or_create(id=1)[0]
                rna.epoca = int(request.POST.get('epoca'))
                rna.save()

                rna.treinar()
            return redirect('home')
