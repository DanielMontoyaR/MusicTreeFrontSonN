import tkinter
import customtkinter
from PIL import ImageTk,Image
import os

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

login = customtkinter.CTk()  #creating cutstom tkinter window
login.geometry("600x440")
login.title('MusicTree')



def main_menu():
    login.withdraw()            # destroy current window and create a new one 
    main_menu = customtkinter.CTk()  
    main_menu.geometry("1280x720")
    main_menu.title('Welcome')
    l1=customtkinter.CTkLabel(master=main_menu, text="Cluster List",font=('Century Gothic',60))
    l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)

    main_menu.protocol("WM_DELETE_WINDOW", lambda: (main_menu.destroy(), login.destroy()))
    main_menu.mainloop()
    






def login_interface():

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.ico")
    login.iconbitmap(icon_path)  # Establece el ícono de la ventana


    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "assets", "pattern.png")

    img1=ImageTk.PhotoImage(Image.open(image_path))
    l1=customtkinter.CTkLabel(master=login,image=img1)
    l1.pack()

    #creating custom frame
    frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
    l2.place(x=50, y=45)

    entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=110)

    entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(x=50, y=165)

    l3=customtkinter.CTkLabel(master=frame, text="Forget password?",font=('Century Gothic',12))
    l3.place(x=155,y=195)

    #Create login button
    button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=main_menu, corner_radius=6)
    button1.place(x=50, y=240)

    #Create sign in button
    button1 = customtkinter.CTkButton(master=frame, width=220, text="Sign In", command=main_menu, corner_radius=6)
    button1.place(x=50, y=300)

    # You can easily integrate authentication system 

    login.mainloop()


login_interface()