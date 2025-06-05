import tkinter
from tkinter import *
from tkinter import colorchooser
import tkinter.colorchooser
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

    #print("ENTRE")

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


            
            cluster_genero_crear_fecha_hora_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            llave_cluster = generar_llave_cluster_unica()

            print("Fecha y hora:", cluster_genero_crear_fecha_hora_creacion)
            print("Llave:", llave_cluster)

            #Aqui se supone que hacemos lo del API ****************888 nombre, descripcion, id, fecha y hora, y una llave id.
            api.crear_cluster(nombre, descripcion, cluster_identificador, cluster_identificador)

        


        else:
            cluster_genero_crear_error_label.configure(text=error_texto)
            cluster_genero_crear_error_label.place(x=10, y=350)

    def regresar():
        #print("regresamos")
        for widget in MusicTreeGUI.winfo_children():
            widget.destroy()
        #cluster_genero_label.destroy()
        main_menu()
        
    def borrar_placeholder(event):
        if cluster_genero_crear_descripcion_entry.get("1.0", "end-1c") == "Descripción (300 caracteres max)":
            cluster_genero_crear_descripcion_entry.delete("1.0", "end")
    
    
    cluster_genero_label = customtkinter.CTkLabel(master=MusicTreeGUI, image=background_image, text="")
    cluster_genero_label.pack()

    cluster_frame = customtkinter.CTkFrame(master=cluster_genero_label, width=500, height=500, corner_radius=15)
    cluster_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
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

    def regresar():
        #print("regresamos")
        for widget in MusicTreeGUI.winfo_children():
            widget.destroy()
        #cluster_genero_ver_label.destroy()
        main_menu()

    def mostrar_cluster(mostrar_inactivos):
        #print("Aqui están")

        for widget in cluster_genero_ver_scroll_frame.winfo_children(): #Se limpia el contenido anterior
            widget.destroy()

        #Este MatTest solo es para pruebas hasta que se implemente todo con el API y la Base
        MatTest = [
            ['C-TKTAIV5XR0ZO', 'Rock Pesado', 'Activo', '2025-05-18 01:51:35'],
            ['C-LYL12629E0FF', 'Alternativo', 'Activo', '2025-05-18 01:52:40'],
            ['C-R3DILYW8CDSE', 'Progresivo', 'Inactivo', '2025-05-18 01:53:57'],
            ['C-XYZABC123456', 'Jazz Fusión', 'Activo', '2025-05-17 14:22:11'],
            ['C-111111111111', 'Metal Melódico', 'Inactivo', '2025-05-16 09:33:01'],
            ['C-222222222222', 'Electrónica', 'Activo', '2025-05-19 16:44:22'],
            ['C-333333333333', 'Reggae Roots', 'Activo', '2025-05-20 17:05:45'],
            ['C-444444444444', 'Indie Pop', 'Activo', '2025-05-15 11:17:33'],
            ['C-555555555555', 'Blues Clásico', 'Inactivo', '2025-05-12 13:27:08'],
            ['C-666666666666', 'Country Rock', 'Activo', '2025-05-11 10:00:00'],
            ['C-777777777777', 'Ska Punk', 'Inactivo', '2025-05-10 18:43:21'],
            ['C-888888888888', 'Synthwave', 'Activo', '2025-05-09 22:11:39'],
            ['C-999999999999', 'Lo-Fi Chill', 'Activo', '2025-05-08 07:56:15'],
        ]


        recieved_list = MatTest #Aqui se supone nos conectamos con la API y recibimos datos

        if not mostrar_inactivos:
            recieved_list = [fila for fila in recieved_list if fila[2] == 'Activo']

        recieved_list.sort(key=lambda x: x[1])  # alfabéticamente ascendente

        
        for i, cluster in enumerate(recieved_list):
            texto = f"{i+1}. ID: {cluster[0]} | Nombre: {cluster[1]} | Estado: {cluster[2]} | Fecha: {cluster[3]}"
            label = customtkinter.CTkLabel(master=cluster_genero_ver_scroll_frame, text=texto, anchor="w")
            label.pack(fill="x", pady=5, padx=10)
            separator = customtkinter.CTkLabel(master=cluster_genero_ver_scroll_frame, text="―" * 100, text_color="black")
            separator.pack(fill="x", pady=(0, 5))
        
        #print(recieved_list)

    #print("Ver Cluster Genero")
    #main_menu()
    cluster_genero_ver_label = customtkinter.CTkLabel(master=MusicTreeGUI, image=background_image, text="")
    cluster_genero_ver_label.pack()

    cluster_genero_ver_frame = customtkinter.CTkFrame(master=cluster_genero_ver_label, width=700, height=600, corner_radius=15)
    cluster_genero_ver_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
    #Label de título
    cluster_genero_ver_titulo_label=customtkinter.CTkLabel(master=cluster_genero_ver_frame, text="Ver Cluster de Género",font=('Century Gothic',20))
    cluster_genero_ver_titulo_label.place(x=150, y=45)

    #Boton de Regresar
    regresarBtn = customtkinter.CTkButton(master=cluster_genero_ver_frame, width=40, text="←", command=regresar, corner_radius=6)
    regresarBtn.place(x=600, y = 10)

    #Boton de ver clusteres
    cluster_genero_ver_btn = customtkinter.CTkButton(master=cluster_genero_ver_frame, width=220, text="Mostrar Clusteres de Género", command=lambda:mostrar_cluster(cluster_genero_ver_inactivos.get()), corner_radius=6)
    cluster_genero_ver_btn.place(x=50, y = 100)

    #RadioButtons para mostrar los Activos / Inactivos
    cluster_genero_ver_inactivos = customtkinter.CTkCheckBox(master=cluster_genero_ver_frame,text="Mostrar Inactivos", command=lambda:mostrar_cluster(cluster_genero_ver_inactivos.get()))
    cluster_genero_ver_inactivos.place(x=280,y=100)

    #ScrollFrame para ver los clusters de género
    cluster_genero_ver_scroll_frame = customtkinter.CTkScrollableFrame(master=cluster_genero_ver_frame, width=600, height=400)
    cluster_genero_ver_scroll_frame.place(x=50, y=150)  # Ajustá el `x` e `y` según el diseño






def genero_crear():
    print("Crear Genero")   
    #main_menu() 
    global genero_crear_color
    genero_crear_color = None

    def regresar():
        print("regresamos")
        for widget in MusicTreeGUI.winfo_children():
            widget.destroy()
        #genero_crear_label.destroy()
        main_menu()

    def borrar_placeholder(event):
        if genero_crear_descripcion_entry.get("1.0", "end-1c") == "Descripción (300 caracteres max)":
            genero_crear_descripcion_entry.delete("1.0", "end")

    def escoger_color():
        global genero_crear_color
        genero_crear_color = tkinter.colorchooser.askcolor(title ="Choose color")
        genero_crear_color = genero_crear_color[1]
        print(str(genero_crear_color))

    def cargar_paises():
        with open("paises.txt", "r", encoding="utf-8") as archivo:
            paises = [linea.strip() for linea in archivo if linea.strip()]
        return paises

    def mostrar_opciones_asociar_cluster(cluster):
        if cluster:
            genero_crear_asociar_cluster_opciones.place(x=10, y=520)
        else:
            genero_crear_asociar_cluster_opciones.place_forget()

    def mostrar_opciones_subgenero(subgenero):
        global genero_crear_color
        #print("mostrando Géneros")
        if subgenero:
            genero_crear_color = None
            genero_crear_color_btn.place_forget()
            genero_crear_asociar_genero_opciones.place(x=10, y=620)
            genero_crear_asociar_genero_label.place(x=10, y=600)
        else:
            genero_crear_color_btn.place(x=325, y=75)
            genero_crear_asociar_genero_opciones.place_forget()
            genero_crear_asociar_genero_label.place_forget()

    def validar_entrada_numerica(input_text):
        # Permite cadena vacía (para borrar) o números entre 0 y 99
        if input_text == "":
            return True
        try:
            numero = int(input_text)
            return 0 <= numero <= 99
        except ValueError:
            return False
        
    def validar_BPM(input_text):
        # Permite cadena vacía (para borrar) o números entre 0 y 250
        if input_text == "":
            return True
        try:
            numero = int(input_text)
            return 0 <= numero <= 250
        except ValueError:
            return False  

    def validar_rango_negativo(input_text):
        if input_text == "" or input_text == "-":  # Permite campo vacío o signo negativo
            return True
        try:
            numero = float(input_text)
            return -60 <= numero <= 0
        except ValueError:
            return False
    
    def validar_duracion(input_text):
        # Permite cadena vacía (para borrar) o números entre 0 y 3600
        if input_text == "":
            return True
        try:
            numero = int(input_text)
            return 0 <= numero <= 3600
        except ValueError:
            return False  

    def generar_llave_identificadora(genero_crear_opcion_subgenero):
        def generar_id_alfanumerico():
            caracteres = string.ascii_uppercase + string.digits
            return ''.join(random.choices(caracteres, k=12))

        id_genero = generar_id_alfanumerico()

        if genero_crear_opcion_subgenero.get():
            id_subgenero = "000000000000"
        else:
            id_subgenero = generar_id_alfanumerico()

        llave = f"G-{id_genero}-S-{id_subgenero}"
        return llave

    def validar_entradas():
        global genero_crear_color
        """
        print("Validando")

        print("Color "+ str(genero_crear_color))

        print("Nombre: " + genero_crear_nombre_entry.get())

        print("Descripción: " + genero_crear_descripcion_entry.get("1.0", "end-1c").strip())

        print("Identificador " + genero_crear_identificador.get())

        print("Promedio de Canciones " + genero_crear_promedio_canciones.get())

        print("Rango de BPM minimo " + genero_crear_BPM_minimo.get())

        print("Rango de BPM maximo " + genero_crear_BPM_maximo.get())

        print("Año de Creación " + genero_crear_año_creacion.get())

        print("Pais de Origen" + genero_crear_paises.get())

        print("Tono dominante " + genero_crear_tonos.get())

        print("Compás " + genero_crear_compas.get())

        print("Volumen Tipico " + genero_crear_volumen_tipico.get())

        print("Duración " + genero_crear_duracion.get())

        print("Cluser " + genero_crear_asociar_cluster_opciones.get())

        print("Genero " + genero_crear_asociar_genero_opciones.get())
        """
        #Parámetros de Género
        color = str(genero_crear_color)
        nombre = genero_crear_nombre_entry.get().strip()
        descripcion = genero_crear_descripcion_entry.get("1.0", "end").strip()
        identificador = genero_crear_identificador.get()
        bpm_minimo = genero_crear_BPM_minimo.get()
        bpm_maximo = genero_crear_BPM_maximo.get()
        año_creacion = genero_crear_año_creacion.get()
        pais_origen = genero_crear_paises.get()
        tono_dominante = genero_crear_tonos.get()
        compas = genero_crear_compas.get()
        volumen_tipico = genero_crear_volumen_tipico.get()
        duracion = genero_crear_duracion.get()
        cluster_asociado = genero_crear_asociar_cluster_opciones.get()
        genero = genero_crear_asociar_genero_opciones.get()
        
        

        error_texto = ""

        if not nombre:
            error_texto = "Error, El campo 'Nombre' es obligatorio"

        if len(nombre) < 3:
            error_texto = "Error, El campo 'Nombre' debe tener al menos 3 caracteres"

        if len(nombre) > 30:
            error_texto = "Error, El campo 'Nombre' no puede tener más de 30 caracteres"

        if len(descripcion) > 1000:
            error_texto = "Error, El campo 'Descripción' no puede tener más de 1000 caracteres"

        if pais_origen == "None":
            error_texto = "Error, No se ha seleccionado País de Origen"

        if año_creacion == "None":
            error_texto = "Error, No se ha especificado el año de Creación"

        if not genero_crear_promedio_canciones.get():
            error_texto = "Error, El campo 'Promedio de Canciones' es Obligatorio"

        #if (genero_crear_asociar_cluster.get()) and (cluster_asociado=="None"):
        #    error_texto = "Error, Se seleccionó asociar cluster, pero no se especificó el cluster"

        if bpm_minimo > bpm_maximo:
            error_texto = "Error, El BPM Mínimo no puede ser mayor al BPM Máximo"
        
        if (color == "None") and (not genero_crear_opcion_subgenero.get()):
            error_texto = "Error, No se ha seleccionado ningún color"

        if (genero_crear_opcion_subgenero.get()) and (genero=="None"):
            error_texto = "Error, Se seleccionó que es subgénero, pero no se seleccionó al género padre"

        if not tono_dominante:
            error_texto = "Error, El campo 'Tono Dominante' es Obligatorio"

        if not volumen_tipico:
            error_texto = "Error, El campo 'Volumen Típico' es Obligatorio"

        if not duracion:
            error_texto = "Error, El campo 'Duración' es Obligatorio"
        #if genero


        if (error_texto ==""): 
            
            if not genero_crear_opcion_subgenero.get():
                genero="None"

            if genero_crear_promedio_canciones.get() == 0:
                promedio_canciones = 0.0
            else:
                promedio_canciones = int(genero_crear_promedio_canciones.get())/100 #Este se hace acá para evitar errores con la división si el espacio es vacío

            #color = str(genero_crear_color)
            #nombre = genero_crear_nombre_entry.get().strip()
            #descripcion = genero_crear_descripcion_entry.get("1.0", "end").strip()
            #identificador = genero_crear_identificador.get()
            #promedio_canciones = genero_crear_promedio_canciones.get()
            #bpm_minimo = genero_crear_BPM_minimo.get()
            #bpm_maximo = genero_crear_BPM_maximo.get()
            #año_creacion = genero_crear_año_creacion.get()
            #pais_origen = genero_crear_paises.get()
            #tono_dominante = genero_crear_tonos.get()
            #compas = genero_crear_compas.get()
            #volumen_tipico = genero_crear_volumen_tipico.get()
            #duracion = genero_crear_duracion.get()
            #cluster_asociado = genero_crear_asociar_cluster_opciones.get()
            #genero = genero_crear_asociar_genero_opciones.get()
            print("Función de validar entradas correcta, Parámetros: \n" +
            "\nNombre: "            + nombre + 
            "\nDescripción: "       + descripcion + 
            "\nIdentificador: "     + identificador +
            "\nColor: "             + color +
            "\nPromedio Canciones: "+ str(promedio_canciones) +
            "\nBPM Mínimo: "        + bpm_minimo +
            "\nBPM Máximo: "        + bpm_maximo +
            "\nAño de Origen: "     + año_creacion +
            "\nPaís de Origen: "    + pais_origen +
            "\nTono Dominante: "    + tono_dominante +
            "\nCompas: "            + compas +
            "\nVolumen Típico"      + volumen_tipico +
            "\nDuración: "          + duracion +
            "\nCluster Asociado:"   + cluster_asociado +
            "\nGénero Asociado:"    + genero)
            genero_crear_error_label.place_forget()

            genero_crear_fecha_hora_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("Fecha y hora:", genero_crear_fecha_hora_creacion)


            llave = generar_llave_identificadora(genero_crear_opcion_subgenero)

            print("La llave es: " + llave)

        else:
            genero_crear_error_label.configure(text=error_texto)
            genero_crear_error_label.place(x=10, y=670)


    
    genero_crear_label = customtkinter.CTkLabel(master=MusicTreeGUI, image=background_image, text="")
    genero_crear_label.pack()

    genero_crear_frame = customtkinter.CTkFrame(master=genero_crear_label, width=400, height=750, corner_radius=15)
    genero_crear_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
    #Label de título
    genero_crear_titulo_label=customtkinter.CTkLabel(master=genero_crear_frame, text="Crear Género",font=('Century Gothic',20))
    genero_crear_titulo_label.place(x=10, y=10)
    
    #Boton de Regresar
    regresarBtn = customtkinter.CTkButton(master=genero_crear_frame, width=40, text="←", command=regresar, corner_radius=6)
    regresarBtn.place(x=350, y = 10)
  
    #Label de error
    genero_crear_error_label = customtkinter.CTkLabel(master=genero_crear_frame, text="",font=('Century Gothic',10), text_color='red')

    #Widgets de Crear Género
    #Entrada de nombre
    genero_crear_nombre_entry = customtkinter.CTkEntry(master=genero_crear_frame, width=300, placeholder_text='Nombre (3-30 caracteres) *')
    genero_crear_nombre_entry.place(x=10,y=75)

    #Entrada de descripción
    #cluster_genero_crear_descripcion_entry = customtkinter.CTkEntry(master=cluster_frame, width=300, height=100, placeholder_text='Descripción (300 caracteres max)')
    #cluster_genero_crear_descripcion_entry.place(x=100,y=125)
    
    genero_crear_descripcion_entry = customtkinter.CTkTextbox(master=genero_crear_frame, width=300, height=100)
    genero_crear_descripcion_entry.insert("1.0", "Descripción (300 caracteres max)")
    genero_crear_descripcion_entry.bind("<FocusIn>", borrar_placeholder)
    genero_crear_descripcion_entry.place(x=10,y=125)
    

    #Boton de Continuar
    genero_crear_continuar_btn = customtkinter.CTkButton(master=genero_crear_frame, width=220, text="Crear Género",command=validar_entradas,corner_radius=6)
    genero_crear_continuar_btn.place(x=10, y=700)

    
    #Selección de Identificador (Activo por defecto)
    
    genero_crear_identificador_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Identificador",font=('Century Gothic',10), text_color='black')
    genero_crear_identificador_label.place(x=10,y=230)

    identificador = ["Activo", "Inactivo"]
    identificador_select = StringVar()
    identificador_select.set(identificador[0])
    genero_crear_identificador = customtkinter.CTkOptionMenu(master=genero_crear_frame, variable=identificador_select,width=100, values=identificador)
    genero_crear_identificador.place(x=10,y=250)



    #Año de creación
    genero_crear_año_creacion_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Año de Creación",font=('Century Gothic',10), text_color='black')
    genero_crear_año_creacion_label.place(x=10,y=280)
    genero_crear_año_creacion = customtkinter.CTkOptionMenu(master = genero_crear_frame, values=[str(year) for year in range(1950, 2026)], width=100)
    genero_crear_año_creacion.set("None")
    genero_crear_año_creacion.place(x=10,y=300)


    #Pais de Origen
    genero_crear_paises_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Pais de Origen",font=('Century Gothic',10), text_color='black')
    genero_crear_paises_label.place(x=10,y=330)
    paises = cargar_paises()
    genero_crear_paises = customtkinter.CTkOptionMenu(master = genero_crear_frame, values=paises, width=200)
    genero_crear_paises.set("None")
    genero_crear_paises.place(x=10,y=350)

    #Modo promedio de canciones.
    genero_crear_promedio_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Promedio de Canciones",font=('Century Gothic',10), text_color='black')
    genero_crear_promedio_label.place(x=150,y=230)
    genero_crear_promedio_label_cero_coma = customtkinter.CTkLabel(master=genero_crear_frame, text="0,",font=('Century Gothic',15), text_color='black')
    genero_crear_promedio_label_cero_coma.place(x=135,y=250)
    genero_crear_promedio_canciones = customtkinter.CTkEntry(master=genero_crear_frame, width=100, placeholder_text="0-99", validate="key", validatecommand=(genero_crear_frame.register(validar_entrada_numerica), "%P"))
    genero_crear_promedio_canciones.place(x=150, y=250)

    
    #Rango de BPM
    genero_crear_BPM_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Rango de BPM",font=('Century Gothic',10), text_color='black')
    genero_crear_BPM_label.place(x=150,y=280)

    genero_crear_BPM_minimo_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Min",font=('Century Gothic',10), text_color='black')
    genero_crear_BPM_minimo_label.place(x=130,y=300)
    genero_crear_BPM_maximo_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Máx",font=('Century Gothic',10), text_color='black')
    genero_crear_BPM_maximo_label.place(x=200,y=300)

    genero_crear_BPM_minimo = customtkinter.CTkEntry(master=genero_crear_frame, width=40, placeholder_text="0-250", validate="key", validatecommand=(genero_crear_frame.register(validar_BPM), "%P"))
    genero_crear_BPM_minimo.place(x=150, y=300)
    genero_crear_BPM_maximo = customtkinter.CTkEntry(master=genero_crear_frame, width=40, placeholder_text="0-250", validate="key", validatecommand=(genero_crear_frame.register(validar_BPM), "%P"))
    genero_crear_BPM_maximo.place(x=222, y=300)




    #Tono musical
    genero_crear_tonos_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Tono Dominante",font=('Century Gothic',10), text_color='black')
    genero_crear_tonos_label.place(x=10,y=380)

    lista_tonos = ["-1","1","2","3","4","5","6","7","8","9","10","11"]
    tonos_select = StringVar()
    tonos_select.set(lista_tonos[0])
    genero_crear_tonos = customtkinter.CTkOptionMenu(master = genero_crear_frame, values=lista_tonos, variable=tonos_select, width=80)
    genero_crear_tonos.place(x=10,y=400)


    #Volumen tipico
    genero_crear_volumen_tipico_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Volumen Típico",font=('Century Gothic',10), text_color='black')
    genero_crear_volumen_tipico_label.place(x=125,y=380)

    genero_crear_volumen_tipico = customtkinter.CTkEntry(master=genero_crear_frame, width=40, placeholder_text="-60 a 0", validate="key", validatecommand=(genero_crear_frame.register(validar_rango_negativo), "%P"))
    genero_crear_volumen_tipico.place(x=125, y=400)


    #Tiempo de Compás
    genero_crear_compas_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Compás",font=('Century Gothic',10), text_color='black')
    genero_crear_compas_label.place(x=10,y=430)

    lista_compas = ["0","2/4","3/4","4/4","5/4","6/4","7/4","8/4"]

    compas_select = StringVar()
    compas_select.set(lista_compas[0])
    genero_crear_compas = customtkinter.CTkOptionMenu(master = genero_crear_frame, values=lista_compas, variable=compas_select, width=80)
    genero_crear_compas.place(x=10,y=450)



    #Duración 
    genero_crear_duracion_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Duración (0-3600 segundos)",font=('Century Gothic',10), text_color='black')
    genero_crear_duracion_label.place(x=125,y=430)

    genero_crear_duracion = customtkinter.CTkEntry(master=genero_crear_frame, width=70, placeholder_text="0 a 3600", validate="key", validatecommand=(genero_crear_frame.register(validar_duracion), "%P"))
    genero_crear_duracion.place(x=125, y=450)



    #Checkbox para asociar o no a un cluster
    genero_crear_asociar_cluster = customtkinter.CTkCheckBox(master=genero_crear_frame,text="Asociar a un Cluster",command=lambda:mostrar_opciones_asociar_cluster(genero_crear_asociar_cluster.get()))
    genero_crear_asociar_cluster.place(x=10,y=490)
    lista_clusters = ["Cluster Rock", "Cluster Metal", "Cluster Rap", "Cluster Trap", "Cluster Progre", "Cluster DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"]#Este es para pruebas hasta que se integre apropiadamente

    genero_crear_asociar_cluster_opciones =  customtkinter.CTkOptionMenu(master = genero_crear_frame, values=lista_clusters, width=200)
    genero_crear_asociar_cluster_opciones.set("None")
    genero_crear_asociar_cluster_opciones.place_forget()



    #Checkbox para escoger si es género o subgénero
    genero_crear_opcion_subgenero = customtkinter.CTkCheckBox(master=genero_crear_frame,text="Es Subgénero", command=lambda:mostrar_opciones_subgenero(genero_crear_opcion_subgenero.get()))
    genero_crear_opcion_subgenero.place(x=10,y=570)

    #Widgets asociados a subgénero
    #Lista de géneros creados para asociar el subgénero
    genero_crear_asociar_genero_label = customtkinter.CTkLabel(master=genero_crear_frame, text="Asocielo a un Género",font=('Century Gothic',10), text_color='black')
    genero_crear_asociar_genero_label.place_forget()

    lista_generos = ["Genero Rock", "Genero Metal", "Genero Rap", "Genero Trap", "Genero Progre", " Genero DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"]#Este es para pruebas hasta que se integre apropiadamente
    genero_crear_asociar_genero_opciones =  customtkinter.CTkOptionMenu(master = genero_crear_frame, values=lista_generos, width=200)
    genero_crear_asociar_genero_opciones.set("None")
    genero_crear_asociar_genero_opciones.place_forget()

    

    #Color (Se oculta si es subgénero, se muestra si es género)
    genero_crear_color_btn =customtkinter.CTkButton(master=genero_crear_frame, width=50, text="Color",command = escoger_color, corner_radius=6)
    genero_crear_color_btn.place(x=325, y=75)















def main_menu():

    def accion_boton(opcion):

        for widget in MusicTreeGUI.winfo_children():
            widget.destroy()
        #mainMenuLabel.destroy()
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
    
    #MusicTreeGUI.geometry("1280x850")
    centrar_ventana(MusicTreeGUI, 1280, 850)
    
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
        #api.verificar_credenciales(name, password)
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