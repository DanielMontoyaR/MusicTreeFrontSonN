import tkinter
import customtkinter
from PIL import ImageTk,Image
import os

import warnings
warnings.filterwarnings("ignore", message="CTkLabel Warning: Given image is not CTkImage*", category=UserWarning)


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

global MusicTreeGUI
global background_image
MusicTreeGUI = customtkinter.CTk()  #creating cutstom tkinter window

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "logo.ico")
base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "images", "pattern.png")
background_image=ImageTk.PhotoImage(Image.open(image_path))


def mainMenu():

    MusicTreeGUI.geometry("1280x720")
    
    mainMenuLabel = customtkinter.CTkLabel(master=MusicTreeGUI, image=background_image, text="")
    mainMenuLabel.pack()


    menuFrame = customtkinter.CTkFrame(master=mainMenuLabel, width=500, height=500, corner_radius=15)
    menuFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=menuFrame, text="Bienvenido USERNAME",font=('Century Gothic',20))
    l2.place(x=150, y=45)


    def esconderMenuBtn():
        generoCrearBtn.place_forget()
        clusterGeneroVerBtn.place_forget()
        clusterGeneroCrearBtn.place_forget()
        cerrarSesionBtn.place_forget()


    def clusterGeneroCrear():
        l2.configure(text= "Crear Cluster de Genero")
        regresarBtn.place(x=450, y = 10)
        esconderMenuBtn()
        

    def clusterGeneroVer():
        l2.configure(text= "Ver Clusteres de Género")
        regresarBtn.place(x=450, y = 10)
        esconderMenuBtn()

    def generoCrear():
        l2.configure(text= "Crear Género")
        regresarBtn.place(x=450, y = 10)
        esconderMenuBtn()

    def firstVisual():
        l2.configure(text= "Bienvenido USERNAME")
        regresarBtn.place_forget()

        clusterGeneroCrearBtn.place(x=150, y=140)
        clusterGeneroVerBtn.place(x=150, y=200)
        generoCrearBtn.place(x=150, y=260)
        cerrarSesionBtn.place(x=0, y=0)

    def cerrar_sesion():
        for widget in MusicTreeGUI.winfo_children():
            widget.destroy()
        loginInterface()


    #Boton de Crear Clúster de Género
    clusterGeneroCrearBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Crear Cluster de Género", command=clusterGeneroCrear, corner_radius=6)
    #Boton de Ver Clústeres de Género
    clusterGeneroVerBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Ver Cluster de Género", command=clusterGeneroVer, corner_radius=6)
    #Boton de Crear Género
    generoCrearBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Crear Género", command=generoCrear, corner_radius=6)
    #Boton de Regresar
    regresarBtn = customtkinter.CTkButton(master=menuFrame, width=40, text="←", command=firstVisual, corner_radius=6)
    #Boton de Cerrar Sesión
    cerrarSesionBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Cerrar Sesión", command=cerrar_sesion, corner_radius=6)

    firstVisual()
    # Cierra ambas ventanas cuando se cierre la nueva
    MusicTreeGUI.protocol("WM_DELETE_WINDOW", MusicTreeGUI.destroy)


def loginInterface():

    MusicTreeGUI.geometry("600x440")
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


    def loginFunction():
        loginLabel.destroy()
        mainMenu()

    def claveOlvidada(event=None):
        print("hola me olvidé la contraseña")


    claveOlvidadaLabel=customtkinter.CTkLabel(master=loginFrame, text="Olvidó su contraseña?",font=('Century Gothic',12))
    claveOlvidadaLabel.place(x=155,y=195)
    claveOlvidadaLabel.bind("<Button-1>", claveOlvidada)
    claveOlvidadaLabel.configure(cursor="hand2")

    #Create login button
    loginBtn = customtkinter.CTkButton(master=loginFrame, width=220, text="Ingresar", command=loginFunction, corner_radius=6)
    loginBtn.place(x=50, y=240)

    #Create sign in button
    signinBtn = customtkinter.CTkButton(master=loginFrame, width=220, text="Crear cuenta", command=loginFunction, corner_radius=6)
    signinBtn.place(x=50, y=300)

    # You can easily integrate authentication system 
    MusicTreeGUI.mainloop()


loginInterface()