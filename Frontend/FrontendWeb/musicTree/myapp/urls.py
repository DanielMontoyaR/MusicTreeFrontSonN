from django.urls import path
from . import views


urlpatterns=[
    path("home/",views.home,name="home"),
    path("todos/", views.todos, name="Todos"),
    path("main_menu/", views.main_menu, name="main_menu"),
    path("crear_cluster/",views.crear_cluster, name="crear_cluster"),
    path("get_cluster_genero/", views.get_cluster_genero, name="get_clusters"),
    path("crear_genero_musica/", views.crear_genero_musica, name="crear_genero_musica")
]