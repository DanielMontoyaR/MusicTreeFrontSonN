from django.urls import path
from . import views


urlpatterns=[
    path("home/",views.home,name="home"),
    path("todos/", views.todos, name="Todos"),
    path("main_menu/", views.main_menu, name="main_menu"),
    path("crear_cluster/",views.crear_cluster, name="crear_cluster"),
    path("ver_cluster_genero/", views.ver_cluster_genero, name="ver_cluster_genero"),
    path("crear_genero_musica/", views.crear_genero_musica, name="crear_genero_musica")
]