from django.shortcuts import render, HttpResponse, redirect 
from django.db.models import Count
from django.contrib import messages
from box.models import *
from datetime import date,timedelta 

import bcrypt


def home(request):
    if "id" in request.session:
        user_id = request.session['id']
        nombre = User.objects.filter(id=user_id)
        context = {
            'nombre' : nombre[0].first_name ,
        }
        return render(request, 'home.html',context=context)
    return render(request, 'home.html')

def register(request):
    print(request.POST)
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
                return redirect ('/register')
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=password,birth_date=request.POST['birth'])
        request.session['id'] = user.id
        print(user.id)
        return redirect('/')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST["login_email"])
        if len(user) == 1:
            if bcrypt.checkpw(request.POST['login_password'].encode(), user[0].password.encode()):
                request.session['email'] = request.POST["login_email"]
                request.session['id'] = user[0].id
                request.session['nombre'] = user[0].first_name
                print(request.session['email'])
                return redirect('/')
        return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")



def obtener_semana():
    today = date.today()
    dias_semana = (6-today.weekday())
    start = None
    end = None
    if today.weekday() > 4:
        if dias_semana == 1:
            start = today+timedelta(days=2)
            end = start+timedelta(days=5)
        else:
            start = today+timedelta(days=1)
            end = start+timedelta(days=5)
        return {"start":start , "end":end}
    else:
        dias_semana = (6-dias_semana)*-1
        start = today+timedelta(days=dias_semana)
        end = start+timedelta(days=5)
        return {"start":start , "end":end}

def horario_dia(request,dia):
    if request.session.get('email') == None:
        return render(request, 'horario.html')
    dia_buscando = int(dia)
    semana = obtener_semana()
    clases = diaclase.objects.filter(dia_clase__range=[semana["start"], semana["end"]])
    semana_clase = []
    for x in clases:
        dia = str(x.dia_clase).split('-')
        convertir = date(int(dia[0]),int(dia[1]),int(dia[2]))
        if convertir.weekday() == dia_buscando:
            semana_clase.append(x)
    context = {
        "clases" : semana_clase,
        "dia" : dia_buscando, 
    }
    return render(request, 'horario.html',context=context)


def planes(request):
    return render(request, 'planes.html')

def tomar_clases(request):
    if request.method == 'POST':
        clase_id=request.POST["clase_id"]
        print(clase_id)
        clase_tomada = diaclase.objects.filter(id=clase_id)
        if clase_tomada:
            usuario = User.objects.filter(id=request.session['id'])
            if usuario:
                print(clase_tomada[0].lista_estudiante)
                clase_tomada[0].lista_estudiante.add(usuario[0])
            url = "horarios/" + request.POST["dia_id"]
            return redirect(url)
    return render(request, 'horario.html')


def store(request):
    if request.session.get('email') == None:
        return render(request, 'store.html')
    if request.method == 'POST':
        print(request.POST["mensualidad"])
        mensualidad = request.POST["mensualidad"]
        id = request.session['id']
        user = User.objects.get(id=id)
        compra = Shop.objects.create(mensualidad=mensualidad,pagado=user)
        return render(request, 'store.html')
    return render(request, 'store.html')

def compras(request):
    shoping = Shop.objects.all()
    context = {
        "shoping" : shoping
    }
    return render(request, 'compras.html', context=context) 

def delete(request,id):
    user_id=request.session.get('id')
    items=Shop.objects.get(id=id)
    items.delete()
    return redirect("/compras")
