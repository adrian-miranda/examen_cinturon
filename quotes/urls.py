from django.urls import path
from . import views

urlpatterns = [
    path('' , views.quotes),
    path('crearMensaje/<int:id>', views.crearMensaje),
    path('crearComentario/<int:id>', views.crearComentario),
    path('delete/<int:id>' , views.delete),
    path('usuario/<int:id>' , views.usuario),
]