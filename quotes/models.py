from django.db import models
from login.models import User


class MensajeManager(models.Manager):
    def validacion(self, postData):
        erroresMensaje={}
        if len(postData['autor']) < 3:
            erroresMensaje['len_autor'] = 'El campo autor debe tener a lo menos 3 caracteres'
        if len(postData['quote']) < 10: 
            erroresMensaje['len_quote'] = 'El campo Quote debe tener a lo menos 10 caracteres'
        return erroresMensaje
class Mensaje(models.Model):
    usuario = models.ForeignKey(User, related_name='mensajes', on_delete= models.CASCADE)
    autor = models.TextField()
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MensajeManager()

    def __repr__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\n'
    def __str__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\n'

class Comentario(models.Model):
    usuario = models.ForeignKey(User, related_name='comentarios_user', on_delete= models.CASCADE)
    mensaje = models.ForeignKey(Mensaje, related_name='comentarios_mensaje', on_delete= models.CASCADE)
    comentario = models.TextField(default='Mensaje Vacio')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\nComentario: {self.comentario}'
    def __str__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\nComentario: {self.comentario}'
