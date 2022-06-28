"""chazam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.base import views
#from django.conf.urls import url

urlpatterns = [
    path('', views.mainPage),
    path('loginPage/', views.login),
    path('updateCoordinates/', views.updateCoordinates),
    path('finalSignup/', views.finalSignup),
    path('uploadChazaInfo/', views.uploadChazaInfo),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('formComensales/',views.form_comensales),
    path('catalogo/',views.filtroChazas),
    path('mapa/',views.mapa),
    path('ranking/', views.rankingView),
    path('formChaza/',views.form_chaza),
    path('eraseChaza/',views.eraseChaza),
    path('setChazaLocation/',views.setChazaLocation),
    path('eraseComment/<int:id>',views.comment_delete, name = 'eraseComment'),
    path('chaza/<slug:slug>/',views.chaza_view.as_view(), name = 'chazaCustom'),
    # path('page-delete/<int:id>', views.delete_object_function, name='delete_object'),
    #url(r'^delete/(?P<pk>[0-9]+)/$', views.comment_delete, name='comment_delete')
]

urlpatterns += staticfiles_urlpatterns()