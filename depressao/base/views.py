from django.shortcuts import render, redirect
import datetime


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
        import ipdb
        ipdb.set_trace()
        return redirect('resultados')
    return render(request, 'app/perguntas.html', {'error': error})


def resultados(request):
    return render(request, 'app/resultados.html')
