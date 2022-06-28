from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse

def userIsOwner(userId):
    isOwner = False
    try:
        customer = comensales.objects.get(IdComensal_id = userId)
        if customer.IdTipoUsuario_id == 2:
            isOwner = True
    except:
        pass
    return isOwner

# Vistas
def login(request):
    return render(request, 'goToLogin.html')
    
def finalSignup(request):
    idActual = str(request.user.id)
    o = comensales.objects.raw("SELECT * from base_comensales where RegistroFinal = "+idActual)
    count = 0
    for obj in o:
        count += 1
    if count != 0:
        return redirect(mainPage)
    else:
        return redirect(form_comensales)

@login_required
def mainPage(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    return render(request, 'mainPage.html', {'user_is_owner': userIsOwner(idActual)})

def form_comensales(request):
    if request.method == 'POST':
        obj = comensales(request.user.id)
        form = comensalesForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            obj.RegistroFinal = obj.IdComensal_id
            obj.save()
            return redirect(mainPage)
        else:
            context = {'form': form }      
            return render(request, 'finalSignup.html', context)
    else:
         tempUsername = request.user.username
         form = comensalesForm(initial={'NombreUsuario': tempUsername, 'IdTipoUsuario':1})
         context = {'form': form}
         return render(request, 'finalSignup.html', context)


def comment_delete(request, id):
    try:
        #Borra los registros de la chaza en la base de datos
        idActual = str(request.user.id)
        instance = comentarios.objects.get(IdChaza=id, IdComensal = idActual)
        chacita = chaza.objects.get(IdChaza=id)
        instance.delete()    
    except:
        pass
    return redirect('../chaza/'+ str(chacita.slug))

@login_required
def form_chaza(request ):
    idActual = str(request.user.id)
    if request.method == 'POST':
        #Revisa si el dueño ya tiene una chaza creada
        o = comensales.objects.raw("SELECT * from base_duenochaza where IdComensal_id = "+idActual)
        count = 0
        for obj in o:
            count += 1
        #Si la chaza ya existe, se modifican sus valores
        if count != 0:
            obj0 = DuenoChaza.objects.get(IdComensal_id = idActual)
            obj = chaza.objects.get(IdChaza = obj0.IdChaza_id)
            form = chazaForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                obj.save()
                return redirect(setChazaLocation)
            return HttpResponse(status=204)
        #Si la chaza no existe, se crea desde 0
        else:
            obj = chaza()
            obj.Puntuacion = 0
            obj2 = DuenoChaza()
            form = chazaForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                obj.save()
                obj2.IdChaza_id = obj.IdChaza
                obj2.IdComensal_id = request.user.id
                obj2.save()
                return redirect(setChazaLocation)
            return HttpResponse(status=204)
            
    else:
        idActual = str(request.user.id)
        #Cuando se abre, trata de buscar los datos de la chaza
        user_has_chaza = False
        try:
            obj0 = DuenoChaza.objects.get(IdComensal_id = idActual)
            obj = chaza.objects.get(IdChaza = obj0.IdChaza_id)  
            tempName = obj.NombreChaza
            tempDescription = obj.Descripcion
            tempUbicacion = obj.IdUbicacion
            tempCategoria = obj.IdCategoria
            form = chazaForm(initial={'NombreChaza': tempName, 'Descripcion': tempDescription, 'IdUbicacion': tempUbicacion, 'IdCategoria': tempCategoria})
            user_has_chaza = True
        #Si no hay datos de la chaza, crea el form por defecto
        except:
            form = chazaForm()
        context = {'form': form, 'user_has_chaza': user_has_chaza}
        return render(request, 'uploadChazaInfo.html', context)

@login_required
def uploadChazaInfo(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    user_is_owner = userIsOwner(idActual)
    if user_is_owner:
        return redirect(form_chaza)
    #Si el usuario es comensal, no puede subir una chaza
    else:
        return redirect(mainPage)

@login_required
def eraseChaza(request):
    try:
        #Borra los registros de la chaza en la base de datos
        idActual = str(request.user.id)
        instance = DuenoChaza.objects.get(IdComensal_id=idActual)
        tempIdChaza = instance.IdChaza_id
        instance.delete()
        instance2 = chaza.objects.get(IdChaza = tempIdChaza)
        instance2.delete()
    except:
        pass
    return redirect(mainPage)

@login_required()
def filtroChazas(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    user_is_owner = userIsOwner(idActual)
    chazas = chaza.objects.all()
    filtro = FiltroChazas(request.GET, queryset=chazas)
    chazas = filtro.qs
    context = {"filtro": filtro, "chazas":chazas, 'user_is_owner': user_is_owner}
    return render(request,"catalogo.html",context)

@login_required()
def rankingView(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    
    user_is_owner = userIsOwner(idActual)
    chazas = chaza.objects.all().order_by("-Puntuacion")
    filtro = FiltroChazas(request.GET, queryset=chazas)
    chazas = filtro.qs
    context = {"filtro": filtro, "chazas":chazas, 'user_is_owner': user_is_owner}
    #obtengo todos los objs de tabla categorias
    context['categorias'] = categoria.objects.all()
    return render(request,"ranking.html",context)


@method_decorator(login_required, name='dispatch')
class chaza_view(DetailView):
    #self.object --> chaza a reseñar
    template_name = 'chazaCustom.html'
    model = chaza
    def post(self,request,*args, **kwargs): 
        self.object = self.get_object()
        form = resenasForm(request.POST)
        comentariosChaza = comentarios.objects.filter(IdChaza_id = self.object.IdChaza)
        commentExists = False
        
        if form.is_valid():
            try:
                comentario = comentarios.objects.get(IdComensal_id = request.user.id, IdChaza_id = self.object.IdChaza )
                commentExists = True
            except:
                comentario =  comentarios(IdChaza_id=self.object.IdChaza, IdComensal_id = request.user.id)  
            form = resenasForm(request.POST, instance = comentario)
            comentario.save()
            form.save()  
            return redirect('/chaza/'+ str(self.object.slug))
        return HttpResponse(status=204)
        
    def get(self,request,*args, **kwargs):
        self.object = self.get_object()
        commentExists = False
        try:
            comentario = comentarios.objects.get(IdComensal_id = request.user.id, IdChaza_id = self.object.IdChaza)
            form = resenasForm(initial={'DescripcionComentario': comentario.DescripcionComentario, 'PuntuacionDada': comentario.PuntuacionDada})
            commentExists = True
        except:
            form = resenasForm()
        comentariosChaza = comentarios.objects.filter(IdChaza_id = self.object.IdChaza)
        context = self.get_context_data(object = self.object, form = form, owner=userIsOwner(request.user.id), comentariosChaza = comentariosChaza, commentExists=commentExists)

        return self.render_to_response(context)

    def get_context_data(self,form,owner,commentExists, **kwargs):
            context = super().get_context_data(**kwargs)
            context['form'] = form
            context['user_is_owner'] = owner
            context['commentExists'] = commentExists
            return context

@login_required()
def mapa(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    user_is_owner = userIsOwner(idActual)
    chazas = chaza.objects.all()
    filtro = FiltroChazas(request.GET, queryset=chazas)
    chazas = filtro.qs
    context = {"filtro": filtro, "chazas":chazas, 'user_is_owner': user_is_owner}
    return render(request,"mapa.html",context)   


@login_required
def setChazaLocation(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    user_is_owner = userIsOwner(idActual)
    if user_is_owner:
        #Busca la chaza
        obj0 = DuenoChaza.objects.get(IdComensal_id = idActual)
        obj = chaza.objects.get(IdChaza = obj0.IdChaza_id)
        context = {'user_is_owner': user_is_owner, 'chaza': obj}
        return render(request,"setChazaLocation.html",context) 
    #Si el usuario es comensal, no puede ingresar
    else:
        return redirect(mainPage)

@login_required()
def updateCoordinates(request):
    #Mira si el usuario actual es dueño o comensal
    idActual = str(request.user.id)
    user_is_owner = userIsOwner(idActual)
    if user_is_owner:
        X = request.GET.get('CoorX')
        Y = request.GET.get('CoorY')
        #Busca la chaza
        obj0 = DuenoChaza.objects.get(IdComensal_id = idActual)
        obj = chaza.objects.get(IdChaza = obj0.IdChaza_id)
        #Actualiza las coordenadas de la chaza
        obj.CoordenadaX = X
        obj.CoordenadaY = Y
        obj.save()