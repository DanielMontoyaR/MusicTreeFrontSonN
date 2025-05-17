import tkinter
import customtkinter
from PIL import ImageTk,Image
import os

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

login = customtkinter.CTk()  #creating cutstom tkinter window
login.geometry("600x440")
login.title('MusicTree')

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "logo.ico")
login.iconbitmap(icon_path) 



def main_menu():

    # En vez de cerrar la ventana anterior de inmediato, solo ábrela como una subventana
    main_menu = customtkinter.CTkToplevel()
    main_menu.geometry("1280x720")
    main_menu.title('Music Tree')
    main_menu.iconbitmap(icon_path)

    # Cargar imagen localmente dentro de esta función
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "pattern.png")
    background_image = ImageTk.PhotoImage(Image.open(image_path))

    mainMenuLabel = customtkinter.CTkLabel(master=main_menu, image=background_image, text="")
    mainMenuLabel.image = background_image  # Mantener referencia viva
    mainMenuLabel.pack()

    menuFrame = customtkinter.CTkFrame(master=mainMenuLabel, width=500, height=500, corner_radius=15)
    menuFrame.place(relx=0.0, rely=0.5, anchor='w')

    l2=customtkinter.CTkLabel(master=menuFrame, text="Bienvenido USERNAME",font=('Century Gothic',20))
    l2.place(x=150, y=45)


    def esconderMenuBtn():
        generoCrearBtn.place_forget()
        clusterGeneroVerBtn.place_forget()
        clusterGeneroCrearBtn.place_forget()


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



    #Boton de Crear Clúster de Género
    clusterGeneroCrearBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Crear Cluster de Género", command=clusterGeneroCrear, corner_radius=6)
    #Boton de Ver Clústeres de Género
    clusterGeneroVerBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Ver Cluster de Género", command=clusterGeneroVer, corner_radius=6)
    #Boton de Crear Género
    generoCrearBtn = customtkinter.CTkButton(master=menuFrame, width=220, text="Crear Género", command=generoCrear, corner_radius=6)
    regresarBtn = customtkinter.CTkButton(master=menuFrame, width=40, text="←", command=firstVisual, corner_radius=6)

    firstVisual()
    # Cierra ambas ventanas cuando se cierre la nueva
    main_menu.protocol("WM_DELETE_WINDOW", lambda: (main_menu.destroy(), login.destroy()))
    login.withdraw()


def login_interface():

    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "images", "pattern.png")
    backgroundImage=ImageTk.PhotoImage(Image.open(image_path))
    

    loginLabel=customtkinter.CTkLabel(master=login,image=backgroundImage)
    loginLabel.pack()

    #creating custom frame
    frame=customtkinter.CTkFrame(master=loginLabel, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=frame, text="Ingrese su cuenta",font=('Century Gothic',20))
    l2.place(x=50, y=45)

    entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Usuario')
    entry1.place(x=50, y=110)

    entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Contraseña', show="*")
    entry2.place(x=50, y=165)

    l3=customtkinter.CTkLabel(master=frame, text="Olvidó su contraseña?",font=('Century Gothic',12))
    l3.place(x=155,y=195)

    #Create login button
    button1 = customtkinter.CTkButton(master=frame, width=220, text="Ingresar", command=main_menu, corner_radius=6)
    button1.place(x=50, y=240)

    #Create sign in button
    button1 = customtkinter.CTkButton(master=frame, width=220, text="Crear cuenta", command=main_menu, corner_radius=6)
    button1.place(x=50, y=300)

    # You can easily integrate authentication system 

    login.mainloop()


login_interface()