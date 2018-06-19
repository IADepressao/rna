from django.shortcuts import render, redirect
from .models import RNA, Neuronio, Erro
import datetime
import json
import numpy as np
import random
import io


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
        rna = RNA.objects.get_or_create(id=1)[0]
        rna.executar()
        return redirect('resultados')
    return render(request, 'app/perguntas.html')


def resultados(request):
    if request.method == 'GET':
        # qs = Erro.objects.all()
        # for e in qs:
        #     memfile = io.BytesIO()
        #     memfile.write(json.loads(e.valores).encode('latin-1'))
        #     memfile.seek(0)
        #     erro = np.load(memfile)

        #     import ipdb
        #     ipdb.set_trace()
        #     pass

        # i = [i for i in range(qs.count())]
        x = np.random.rand(5)
        y = np.random.rand(5)
        index = [i for i in range(5)]

        context = {

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
                rna = RNA.objects.get_or_create(id=1)[0]
                rna.epoca = abs(int(request.POST.get('epoca')))
                rna.save()

                rna.executar(testar=True)
            return redirect('home')
