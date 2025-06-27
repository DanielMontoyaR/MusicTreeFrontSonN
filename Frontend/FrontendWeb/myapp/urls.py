from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
#from . import views
from .vistas import vista_home 
from .vistas import vista_menu
from .vistas import vista_genero
from .vistas import vista_cluster
from .vistas import vista_artista
from .vistas import vista_fanatico



urlpatterns=[
    path('', lambda request: redirect('home/', permanent=False)),

    path("home/", vista_home.home, name="home"),
    path("main_menu/", vista_menu.main_menu, name="main_menu"),
    path("fanatico_menu/", vista_menu.fanatico_menu, name="fanatico_menu"),
    #Cluster
    path("crear_cluster/", vista_cluster.crear_cluster, name="crear_cluster"),
    path("get_cluster_genero/", vista_cluster.get_cluster_genero, name="get_clusters"),
    path("api/clusters/", vista_genero.get_clusters, name='get_clusters'),
    #Genero
    path("crear_genero_musica/", vista_genero.crear_genero_musica, name="crear_genero_musica"),
    path("importar_generos/", vista_genero.importar_generos, name="importar_generos"),
    path("api/genres/", vista_genero.get_genres, name='get_genres'),
    
    #Artista
    path("registrar_artista/", vista_artista.registrar_artista, name="registrar_artista"),
    path("ver_artista/",vista_artista.ver_artista, name="ver_artista"),
    path("ver_catalogo_artista/", vista_artista.ver_catalogo_artista, name="ver_catalogo_artista"),
    path("api/subgenres/", vista_artista.get_subgenres, name = "get_subgenres"),
    path("buscar_artista_genero/", vista_artista.buscar_artista_por_genero, name= "buscar_artista_genero"),
    
    #Fanatico
    path("registrar_fanatico/", vista_fanatico.registrar_fanatico, name="registrar_fanatico"),
    path("login_fanatico/", vista_fanatico.login_fanatico, name="login_fanatico"),
    path("ver_generos/",vista_fanatico.ver_generos, name="ver_generos"),
    
]