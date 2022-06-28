from email.mime import base
from django import forms
from django.forms import ChoiceField
from .models import *
import django_filters
from django import forms
from django_filters import  *
from django.db.models import Q
from django.forms import TextInput

# Para filtrar chazas --> pip install django-filter
class FiltroChazas(django_filters.FilterSet):
    class Meta:
        model = chaza
        fields = [
            'NombreChaza', 
            'Descripcion',
            'IdCategoria',
            'Puntuacion']

    CHOICES_CATEGORIAS = []
    CHOICES_UBICACIONES = []
    CHOICES_PUNTUACIONES = [(1,"0 - 1"),(2,"1 - 2"),(3,"2 - 3"),(4,"3 - 4"),(5,"4 - 5")]
    # Obtengo todas las categorias y las ubicaciones y las meto a sus CHOICES
    categorias = categoria.objects.all()
    ubicaciones = Ubicaciones.objects.all()
    # print(categorias)
    
    
    i = 1
    for IdCategoria in categorias:
        CHOICES_CATEGORIAS.append((i,IdCategoria))
        # print(IdCategoria)
        i+=1
    i = 1
    for IdUbicacion in ubicaciones:
        CHOICES_UBICACIONES.append((i,IdUbicacion))
        # print(IdUbicacion)
        i+=1
    
    # Personalizo los filtros
    Categorias = django_filters.MultipleChoiceFilter(
        label='Categorias',
        choices = CHOICES_CATEGORIAS,
        widget = forms.CheckboxSelectMultiple(),
        method = 'Categorias_method'
        )
    
    CategoriasRanking =  django_filters.ChoiceFilter(
        label='CategoriasRanking',
        choices = CHOICES_CATEGORIAS,
        method = 'CategoriasRanking_method'
        )

    Ubicaciones = django_filters.MultipleChoiceFilter(
        label='Ubicaciones',
        choices = CHOICES_UBICACIONES,
        widget = forms.CheckboxSelectMultiple(),
        method = 'Ubicaciones_method'
        )
    Puntuaciones = django_filters.MultipleChoiceFilter(
        label='Puntuaciones',
        choices = CHOICES_PUNTUACIONES,
        widget = forms.CheckboxSelectMultiple(),
        method = 'Puntuaciones_method'
        )
    
    my_lookup_field = django_filters.CharFilter(
        label='Chaza', 
        method='my_lookup_method',
        widget=TextInput(attrs={
            'placeholder': 'Inserta el nombre de la chaza o una palabra clave (Ej: postres, hamburguesas...)',
             'class': "searchField"
             })
    )
    
    # Métodos :3
    def Categorias_method(self, queryset, name, value):
        return queryset.filter((Q(IdCategoria__in=value))) 

    def CategoriasRanking_method(self, queryset, name, value):
        return queryset.filter((Q(IdCategoria__in=value))).order_by("Puntuacion").reverse()  
    
    def Ubicaciones_method(self, queryset, name, value):
        return queryset.filter((Q(IdUbicacion__in=value)))    
    
    def Puntuaciones_method(self, queryset, name, value):
        # Crea un queryset vacío
        newQueryset = chaza.objects.none()
        for tope in value:
            # Por cada casilla marcada, filtra según el rango (es incluyente) y une a "newQueryset"
            tope_num = int(tope)
            newQueryset |= queryset.filter(((Q(Puntuacion__gt=(tope_num-1)) & Q(Puntuacion__lt=tope_num)) | Q(Puntuacion=tope_num)| Q(Puntuacion=(tope_num-1)) ))   
        return newQueryset
        
    def my_lookup_method(self, queryset, name, value):
        return queryset.filter((Q(NombreChaza__icontains=value)|Q(Descripcion__icontains=value)))
    
    
    
