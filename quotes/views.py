from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
from datetime import datetime, time, timedelta
from django.utils import timezone

def quotes(request):
    if 'usuario' not in request.session:
        return redirect('/')
    else:
        mensajes = Mensaje.objects.all().order_by('-created_at')
        cantMensajes = len(mensajes)
        comentarios = Comentario.objects.all()
        cantComentarios =len(comentarios)
        usuarios = User.objects.all()
        contexto = {
            'mensajes'          : mensajes,
            'comentarios'       : comentarios, 
            'usuarios'          : usuarios,
            'cantMensajes'      : cantMensajes,
            'cantComentarios'   : cantComentarios,
        }
        return render(request , 'quotes.html' , contexto)

def crearMensaje(request , id):
    usuario = User.objects.get(id = id)
    erroresMensaje = Mensaje.objects.validacion(request.POST)
    if len(erroresMensaje) > 0:
        for key , value in erroresMensaje.items():
            messages.warning(request , value)
            request.session['mensaje_autor'] = request.POST['autor']
            messages.warning( request,'Usuario Actualizado')
            request.session['mensaje_quote'] = request.POST['quote']
    else:
        mensaje = Mensaje.objects.create(
            usuario = usuario,
            autor = request.POST['autor'],
            mensaje = request.POST['quote'],
        )
    print(request.POST)
    return redirect('/quotes')

def liked(request, id):
    mensaje = Mensaje.objects.get(id = id)
    return redirect('/quotes')

def crearComentario(request, id):
    mensaje = Mensaje.objects.get(id = id)
    usuario_comentador = User.objects.get(id = request.session['usuario']['id'])
    comentario = Comentario.objects.create(
        mensaje = mensaje,
        usuario = usuario_comentador,
    )
    print(request.POST)
    return redirect('/quotes')

def delete(request , id):
    usuario = User.objects.get(id = request.session['usuario']['id'])
    mensaje = Mensaje.objects.get(id = id)
    messages.success(request ,'Borrado con exito')
    mensaje.delete()
    return redirect("/quotes")

def usuario(request , id):
    if 'usuario' not in request.session:
        return redirect('/')
    else:
        usuario = User.objects.get(id = id)
        citas = Mensaje.objects.all()
        usuarios = User.objects.all()
        contexto = {
            'usuarios' : usuarios,
            'citas' : citas,
            'usuario': usuario,
        }
        return render(request, 'usuario.html', contexto)
