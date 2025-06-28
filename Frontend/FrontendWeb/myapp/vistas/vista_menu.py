from django.shortcuts import render

def main_menu(request):
    ruta_main_menu = "Menu/main_menu.html"
    return render(request, ruta_main_menu)

def fanatico_menu(request):
    ruta_fanatico_menu = "Menu/fanatico_menu.html"
    return render(request, ruta_fanatico_menu)