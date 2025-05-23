from django.shortcuts import render


def home(request):
    ruta_home = "Home/home.html"
    return render(request, ruta_home)