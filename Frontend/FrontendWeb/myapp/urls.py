from django.urls import path
#from . import views
from .vistas import vista_home 
from .vistas import vista_menu
from .vistas import vista_genero
from .vistas import vista_cluster
from .vistas import vista_artista



urlpatterns=[
    #path("home/",views.home,name="home"),
    #path("todos/", views.todos, name="Todos"),
    #path("main_menu/", views.main_menu, name="main_menu"),
    #path("crear_cluster/",views.crear_cluster, name="crear_cluster"),
    #path("get_cluster_genero/", views.get_cluster_genero, name="get_clusters"),
    #path("crear_genero_musica/", views.crear_genero_musica, name="crear_genero_musica")
    path("home/", vista_home.home, name="home"),
    path("main_menu/", vista_menu.main_menu, name="main_menu"),
    path("crear_cluster/", vista_cluster.crear_cluster, name="crear_cluster"),
    path("get_cluster_genero/", vista_cluster.get_cluster_genero, name="get_clusters"),
    path("crear_genero_musica/", vista_genero.crear_genero_musica, name="crear_genero_musica"),
    path("importar_generos/", vista_genero.importar_generos, name="importar_generos"),
    path("registrar_artista/", vista_artista.registrar_artista, name="registrar_artista"),
    path("ver_catalogo_artista/", vista_artista.ver_catalogo_artista, name="ver_catalogo_artista"),
    path("api/clusters/", vista_genero.get_clusters, name='get_clusters'),
    path("api/genres/", vista_genero.get_genres, name='get_genres'),
]