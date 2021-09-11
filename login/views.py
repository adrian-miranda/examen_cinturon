from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt
import re

def index(request):
    if request.method  == 'GET':
        contexto = {'titulo' : 'Login/Registro'}
        return render(request , 'index.html' , contexto)

def registrar(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method  == 'POST':
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            for key , value in errores.items():
                messages.warning(request , value)
            request.session['user_first_name'] = request.POST['first_name']
            request.session['user_last_name'] = request.POST['last_name']
            request.session['user_email'] = request.POST['email']
            request.session['user_password'] = request.POST['password']
            request.session['user_password_confirm'] = request.POST['password_confirm']
            return redirect('/')
        else:
            encriptacion = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = encriptacion,
            )
            sesion_de_usuario = {
                    'id' : user.id,
                    'nombre' : user.first_name,
                    'apellido' : user.last_name,
                    'email' : user.email,
                    # aca no se puede guardar un objeto completo , hay que separarlo por partes para que pueda ser tomado
                }
            print(f'el post es: {request.POST}')
            request.session['usuario'] = sesion_de_usuario
            messages.success(request ,'Usuario registrado')
            request.session['user_first_name'] = '' 
            request.session['user_last_name'] = '' 
            request.session['user_email'] = '' 
            request.session['user_password'] = '' 
            request.session['user_password_confirm'] = '' 
            return redirect('/quotes/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method  == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            user_logeado = user[0]
            if bcrypt.checkpw(request.POST['password'].encode() , user_logeado.password.encode()):
                sesion_de_usuario = {
                    'id'         : user_logeado.id,
                    'nombre'     : user_logeado.first_name,
                    'apellido'   : user_logeado.last_name,
                    'email'      : user_logeado.email,
                    'created_at' : user_logeado.created_at.strftime('%Y-%m-%d'),
                    # aca no se puede guardar un objeto completo , hay que separarlo por partes para que pueda ser tomado
                }
                request.session['usuario'] = sesion_de_usuario
                request.session['user_email_login'] = ''
                request.session['user_password_login'] = ''
                return redirect('/quotes/')
            else:
                messages.warning(request ,'Contraseña Invalida')
                request.session['user_email_login'] = request.POST['email']
                request.session['user_password_login'] = request.POST['password']
                return redirect('/')
        else:
            messages.warning(request ,'Correo Invalido')
            request.session['user_email_login'] = request.POST['email']
            request.session['user_password_login'] = request.POST['password']
            return redirect('/')
            

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        return redirect('/')
    else:
        return redirect('/')

def editar(request , id):
    if 'usuario' in request.session:
        usuario = User.objects.filter(id=id)
        contexto = {
            'usuario' : usuario
        }
        if request.method == 'GET':
            usuario = User.objects.filter(id=id)
            print(f'el usuario de la base de datos es: {usuario}')
            contexto = {'titulo': 'Editar',}
            return render(request ,'editar.html' , contexto)
        if request.method == 'POST':
            errores = User.objects.validacion(request.POST)
            if len(errores) > 0:
                for key , value in errores.items():
                    messages.warning(request , value)
                request.session['user_first_name'] = request.POST['first_name']
                request.session['user_last_name'] = request.POST['last_name']
                request.session['user_email'] = request.POST['email']
                request.session['user_password'] = request.POST['password']
                request.session['user_password_confirm'] = request.POST['password_confirm']
                return redirect('/quotes')
            else:
                usuario = User.objects.get(id = id)
                usuario_logueado = request.session['usuario']['id']
                if usuario.id == usuario_logueado:
                    del request.session['usuario']
                    encriptacion = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
                    usuario.first_name = request.POST['first_name']
                    usuario.last_name = request.POST['last_name']
                    usuario.email = request.POST['email']
                    usuario.password = encriptacion
                    usuario.save()
                    messages.success( request,'Usuario Actualizado')
                    request.session['user_first_name'] = ''
                    request.session['user_last_name'] = ''
                    request.session['user_email'] = ''
                    request.session['user_password'] = ''
                    request.session['user_password_confirm'] = ''
                    sesion_de_usuario = {
                    'id' : usuario.id,
                    'nombre' : usuario.first_name,
                    'apellido' : usuario.last_name,
                    'email' : usuario.email,
                    # aca no se puede guardar un objeto completo , hay que separarlo por partes para que pueda ser tomado
                    }
                    request.session['usuario'] = sesion_de_usuario 
                    return redirect('/quotes')
                else:
                    print('los usuarios son diferentes')
                    return redirect('/')
    else:
        return redirect('/')
