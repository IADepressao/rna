from django.shortcuts import render, redirect
from .models import Product
import datetime
import json
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
    Product.objects.all().delete()
    for n in range(10):
         p = Product()
         p.name = "Produto " + str(n)
         p.price = random.randint(1,30)
         p.save()

    queryset = Product.objects.all()
    names = [obj.name for obj in queryset]
    prices = [int(obj.price) for obj in queryset]

    context = {
        'names': json.dumps(names),
        'prices': json.dumps(prices),
    }
    return render(request, 'app/resultados.html', context)


def configuracoes(request):
    if request.method == 'GET':
        return render(request, 'app/configuracoes.html')
    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('home')
        else:
            #update configs
            return redirect('home')
