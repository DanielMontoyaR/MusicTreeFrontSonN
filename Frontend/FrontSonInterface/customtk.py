import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk,Image
import sys
import os
from datetime import datetime
import random
import string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from API import api


import warnings
warnings.filterwarnings("ignore", message="CTkLabel Warning: Given image is not CTkImage*", category=UserWarning)


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

#global MusicTreeGUI
#global background_image
MusicTreeGUI = customtkinter.CTk()  #creating cutstom tkinter window

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "logo.ico")
base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "images", "pattern.png")
background_image=ImageTk.PhotoImage(Image.open(image_path))



def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()  # Asegura que se actualicen las medidas reales de la ventana
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")




def cluster_genero_crear():

    print("ENTRE")
    cluster_genero_label = customtkinter.CTkLabel(master=MusicTreeGUI, image=background_image, text="")
    cluster_genero_label.pack()

    cluster_frame = customtkinter.CTkFrame(master=cluster_genero_label, width=500, height=500, corner_radius=15)
    cluster_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def generar_llave_cluster():
        caracteres = string.ascii_uppercase + string.digits # Letras mayúsculas + dígitos
        clave = ''.join(random.choices(caracteres,k=12))
        return f"C-{clave}"



    claves_generadas = set()

    def generar_llave_cluster_unica():
        while True:
            nueva_clave = generar_llave_cluster()
            if nueva_clave not in claves_generadas:
                claves_generadas.add(nueva_clave)
                return nueva_clave

    def validar_entradas():

        nombre = cluster_genero_crear_nombre_entry.get().strip()
        descripcion = cluster_genero_crear_descripcion_entry.get("1.0", "end").strip()
        cluster_identificador = cluster_genero_crear_descripcion_identificador.get()
        error_texto = ""

        if not nombre:
            error_texto = "Error, El campo 'Nombre' es obligatorio"
        if len(nombre) < 3:
            error_texto = "Error, El campo 'Nombre' debe tener al menos 3 caracteres"
        if len(nombre) > 30:
            error_texto = "Error, El campo 'Nombre' no puede tener más de 30 caracteres"
        if len(descripcion) > 300:
            error_texto = "Error, El campo 'Descripción' no puede tener más de 300 caracteres"

        if (error_texto ==""): 
            print("Función de validar entradas correcta, Parámetros:\nNombre " + nombre + "\nDescripción: " + descripcion + "\nIdentificador: " + cluster_identificador)
            cluster_genero_crear_error_label.place_forget()


            
            fecha_hora_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            llave_cluster = generar_llave_cluster_unica()

            print("Fecha y hora:", fecha_hora_creacion)
            print("Llave:", llave_cluster)

            #Aqui se supone que hacemos lo del API ****************888 nombre, descripcion, id, fecha y hora, y una llave id.
        


        else:
            cluster_genero_crear_error_label.configure(text=error_texto)
            cluster_genero_crear_error_label.place(x=10, y=350)

    def regresar():
        #print("regresamos")
        #for widget in MusicTreeGUI.winfo_children():
        #    widget.destroy()
        cluster_genero_label.destroy()
        main_menu()
        
    def borrar_placeholder(event):
        if cluster_genero_crear_descripcion_entry.get("1.0", "end-1c") == "Descripción (300 caracteres max)":
            cluster_genero_crear_descripcion_entry.delete("1.0", "end")
    #Label de error
    cluster_genero_crear_error_label = customtkinter.CTkLabel(master=cluster_frame, text="",font=('Century Gothic',15), text_color='red')

    #Label de título
    cluster_genero_crear_titulo_label=customtkinter.CTkLabel(master=cluster_frame, text="Crear Cluster de Género",font=('Century Gothic',20))
    cluster_genero_crear_titulo_label.place(x=150, y=45)

    

    #Widgets de crear cluster de género
    #Entrada de nombre
    cluster_genero_crear_nombre_entry = customtkinter.CTkEntry(master=cluster_frame, width=300, placeholder_text='Nombre (3-30 caracteres) *')
    cluster_genero_crear_nombre_entry.place(x=100,y=75)

    #Entrada de descripción
    #cluster_genero_crear_descripcion_entry = customtkinter.CTkEntry(master=cluster_frame, width=300, height=100, placeholder_text='Descripción (300 caracteres max)')
    #cluster_genero_crear_descripcion_entry.place(x=100,y=125)
    
    cluster_genero_crear_descripcion_entry = customtkinter.CTkTextbox(master=cluster_frame, width=300, height=100)
    cluster_genero_crear_descripcion_entry.insert("1.0", "Descripción (300 caracteres max)")
    cluster_genero_crear_descripcion_entry.bind("<FocusIn>", borrar_placeholder)
    cluster_genero_crear_descripcion_entry.place(x=100,y=125)
    

    #Boton de Continuar
    continuar_btn = customtkinter.CTkButton(master=cluster_frame, width=220, text="Crear",command=validar_entradas, corner_radius=6)
    continuar_btn.place(x=100, y=400)


    
    #Selección de Identificador (Activo por defecto)
    identificador = ["Activo", "Inactivo"]
    identificador_select = StringVar()
    identificador_select.set(identificador[0])
    cluster_genero_crear_descripcion_identificador = customtkinter.CTkOptionMenu(master=cluster_frame, variable=identificador_select, values=identificador)
    cluster_genero_crear_descripcion_identificador.place(x=100,y=250)

    #Boton de Regresar
    regresarBtn = customtkinter.CTkButton(master=cluster_frame, width=40, text="←", command=regresar, corner_radius=6)
    regresarBtn.place(x=450, y = 10)


def cluster_genero_ver():
    print("Ver Cluster Genero")
    main_menu()

def genero_crear():
    print("Crear Genero")   
    main_menu() 




def main_menu():

    def accion_boton(opcion):

        #for widget in MusicTreeGUI.winfo_children():
        #    widget.destroy()
        mainMenuLabel.destroy()
        match opcion:
            case 1:
                cluster_genero_crear()
            case 2:
                cluster_genero_ver()
            case 3:
                genero_crear()
            case 4:
                login_interface()
        return
    
    #MusicTreeGUI.geometry("1280x720")
    centrar_ventana(MusicTreeGUI, 1280, 720)
    
    mainMenuLabel = customtkinter.CTkLabel(master=MusicTreeGUI, image=background_image, text="")
    mainMenuLabel.pack()


    menuFrame = customtkinter.CTkFrame(master=mainMenuLabel, width=500, height=500, corner_radius=15)
    menuFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=menuFrame, text="Bienvenido USERNAME",font=('Century Gothic',20))
    l2.place(x=150, y=45)
            
              

    #Boton de Crear Clúster de Género
    clusterGeneroCrearBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Crear Cluster de Género", command=lambda:accion_boton(1), corner_radius=6)
    clusterGeneroCrearBtn.place(x=150, y=140)

    #Boton de Ver Clústeres de Género
    clusterGeneroVerBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Ver Cluster de Género", command=lambda:accion_boton(2), corner_radius=6)
    clusterGeneroVerBtn.place(x=150, y=200)

    #Boton de Crear Género
    generoCrearBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Crear Género", command=lambda:accion_boton(3), corner_radius=6)
    generoCrearBtn.place(x=150, y=260)

    #Boton de Cerrar Sesión
    cerrarSesionBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Cerrar Sesión", command=lambda:accion_boton(4), corner_radius=6)
    cerrarSesionBtn.place(x=0, y=0)

    # Cierra ambas ventanas cuando se cierre la nueva
    MusicTreeGUI.protocol("WM_DELETE_WINDOW", MusicTreeGUI.destroy)







def login_interface():

    def login_function():
        name = entry1.get().strip()
        password = entry2.get().strip()
        loginLabel.destroy()
        api.verificar_credenciales(name, password)
        main_menu()

    def clave_olvidada(event=None):
        print("hola me olvidé la contraseña")



    #MusicTreeGUI.geometry("600x440")
    centrar_ventana(MusicTreeGUI, 600, 440)  # En loginInterface
    MusicTreeGUI.title('MusicTree')
    MusicTreeGUI.iconbitmap(icon_path)



    loginLabel=customtkinter.CTkLabel(master=MusicTreeGUI,image=background_image)
    loginLabel.pack()

    #creating custom frame
    loginFrame=customtkinter.CTkFrame(master=loginLabel, width=320, height=360, corner_radius=15)
    loginFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=loginFrame, text="Ingrese su cuenta",font=('Century Gothic',20))
    l2.place(x=50, y=45)

    entry1=customtkinter.CTkEntry(master=loginFrame, width=220, placeholder_text='Usuario')
    entry1.place(x=50, y=110)

    entry2=customtkinter.CTkEntry(master=loginFrame, width=220, placeholder_text='Contraseña', show="*")
    entry2.place(x=50, y=165)





    claveOlvidadaLabel=customtkinter.CTkLabel(master=loginFrame, text="Olvidó su contraseña?",font=('Century Gothic',12))
    claveOlvidadaLabel.place(x=155,y=195)
    claveOlvidadaLabel.bind("<Button-1>", clave_olvidada)
    claveOlvidadaLabel.configure(cursor="hand2")

    #Create login button
    loginBtn = customtkinter.CTkButton(master=loginFrame, width=220, text="Ingresar", command=login_function, corner_radius=6)
    loginBtn.place(x=50, y=240)

    #Create sign in button
    signinBtn = customtkinter.CTkButton(master=loginFrame, width=220, text="Crear cuenta", command=login_function, corner_radius=6)
    signinBtn.place(x=50, y=300)

    # You can easily integrate authentication system 
    MusicTreeGUI.mainloop()


login_interface()