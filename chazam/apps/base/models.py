from turtle import pos
from django.db import models 
from django.forms import IntegerField 
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import IntegerField, Model
from django.db.models import Avg
import math


# Create your models here.

# class Puntuaciones(models.Model):
#     IdPuntuacion = models.AutoField(primary_key=True)
#     Puntuacion = models.IntegerField(default=0)

class Ubicaciones(models.Model):
    IdUbicacion = models.AutoField(primary_key=True)
    NombreUbicacion = models.CharField(max_length=100, null=False, verbose_name="Ubicacion")
    def __str__(self):
        return self.NombreUbicacion

class categoria(models.Model):
    IdCategoria = models.AutoField(primary_key=True)
    NombreCategoria = models.CharField(max_length=20, blank=False, null=False)
    def __str__(self):
        return self.NombreCategoria


class chaza(models.Model):
    IdChaza = models.AutoField(primary_key=True)
    IdUbicacion = models.ForeignKey(Ubicaciones, on_delete=models.CASCADE,verbose_name="Ubicación")
    IdCategoria = models.ForeignKey(categoria, on_delete=models.CASCADE, verbose_name="Categoria")

    NombreChaza = models.CharField(max_length=40, blank=False, null=False,  verbose_name="Nombre Chaza")
    Puntuacion = models.FloatField(blank=False)
    Descripcion = models.TextField(blank=False, null=False,  verbose_name="Descripción",)
    CoordenadaX = models.CharField(max_length=6,blank=True, null=True, default= "450px")
    CoordenadaY = models.CharField(max_length=6, blank=True, null=True, default= "450px")

    slug= models.SlugField(max_length=255, unique=True, default="default")
    def __str__(self):
        return self.NombreChaza
    def save(self, *args, **kwargs):
        self.slug = slugify(self.NombreChaza)
        super(chaza, self).save(*args, **kwargs)

    def getCategoryName(self):
        obj = categoria.objects.get(IdCategoria = self.IdCategoria_id)
        return obj.NombreCategoria

    def getLocationName(self):
        obj = Ubicaciones.objects.get(IdUbicacion = self.IdUbicacion_id)
        return obj.NombreUbicacion

# class chazaCategoria(models.Model):
#     IdCategoria = models.ForeignKey(categoria, on_delete=models.CASCADE)
#     IdChaza = models.ForeignKey(chaza, on_delete=models.CASCADE)

class tipoUsuario(models.Model):
    IdTipoUsuario = models.AutoField(primary_key=True, )
    NombreTipoUsuario = models.CharField(max_length=30, blank=False, null=False )

    def __str__(self):
        return self.NombreTipoUsuario

class comensales(models.Model):
    IdComensal = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, primary_key=True,unique=True)
    IdTipoUsuario = models.ForeignKey(tipoUsuario, on_delete=models.CASCADE, verbose_name="Tipo de Usuario", default=1)
    NombreUsuario = models.CharField(max_length=20, blank=False, null=False, verbose_name= "Nombre a Mostrar", default= "Superusuario")
    RegistroFinal = models.IntegerField(default=0)
    def __str__(self):
        return self.NombreUsuario

class comentarios(models.Model):
    RATING_RANGE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    IdComentario = models.AutoField(primary_key=True)
    IdComensal = models.ForeignKey(comensales, on_delete=models.CASCADE)
    IdChaza = models.ForeignKey(chaza, on_delete=models.CASCADE, verbose_name="Nombre de la chaza")
    DescripcionComentario= models.TextField(max_length=400, blank=False, null=False, verbose_name="Escribe tu reseña")
    PuntuacionDada = models.IntegerField(blank=False, default=5, verbose_name="Puntuación",  choices=RATING_RANGE)
    def __str__(self):
        return self.IdComentario + "." + self.DescripcionComentario

class DuenoChaza(models.Model):
    IdDuenoChaza = models.AutoField(primary_key=True)
    IdComensal = models.ForeignKey(comensales, on_delete=models.CASCADE)
    IdChaza = models.ForeignKey(chaza, on_delete=models.CASCADE)
    def __str__(self):
        return self.IdDuenoChaza


@receiver(post_save, sender=comentarios)
def update_Puntuacion(sender,instance, **kwargs):
    pkChaza = instance.IdChaza_id
    puntaje = comentarios.objects.filter(IdChaza_id = pkChaza).aggregate( Avg('PuntuacionDada'))
    chazaUpdate = chaza.objects.get(IdChaza= pkChaza)

    chazaUpdate.Puntuacion = round(puntaje['PuntuacionDada__avg'], 2)
    chazaUpdate.save()