from django.shortcuts import render, HttpResponse
from .models import TodoItem
from .models import ClusterGenero
# Create your views here.


def home(request):
    #return HttpResponse("hello world!")
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html",{"todos": items})

def main_menu(request):
    return render(request, "main_menu.html")

def crear_cluster(request):
    return render(request,"crear_cluster.html")

def ver_cluster_genero(request):
    items = ClusterGenero.objects.all()
    return render(request, "ver_cluster_genero.html", {"datos": items})