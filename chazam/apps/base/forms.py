from django.db import models
from django.forms import ModelForm
import django_filters
from .models import *
from django.forms import ModelForm, TextInput,Textarea,Select
from .models import comensales, chaza
from django import forms

class comensalesForm(ModelForm):
    class Meta:
        model = comensales
        fields = ['NombreUsuario', 'IdTipoUsuario']


class chazaForm(ModelForm):
    class Meta:
        model = chaza
 
        fields = ['NombreChaza', 'Descripcion', 'IdUbicacion','IdCategoria']
        widgets = {
            'NombreChaza': TextInput(attrs={
                'class': "form-control"
                }),
            'IdUbicacion': Select(attrs={
                'class': "form-control1"
                }),
            'IdCategoria': Select(attrs={
                'class': "form-control2"
                }),
            'Descripcion': Textarea(attrs={
                'class': "form-control3"
                })
        }
        
        

class resenasForm(ModelForm):
    class Meta:
        model = comentarios
        fields = ['DescripcionComentario', 'PuntuacionDada']
        widgets = {
            'DescripcionComentario': Textarea(attrs={
                'class': "form-control4"
                }),
            'PuntuacionDada': Select(attrs={
                'class': "form-control5"
                })}