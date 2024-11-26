from tkinter import ttk, StringVar
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
from functions import busqueda_por_id, cambiar_tipo_busqueda, borrar_busqueda_name, filtrar_por_tipo_auto, mostrar_detalles_pokemon, abrir_ventana_agregar_pokemon, actualizar_datos

def pestañas(root): 
# -----------------------CREACION DE LA NOTEBOOK----------------------------------------------------
 notebook = ttk.Notebook(root)
 notebook.place(x=0, y=0, width=550, height=700)
#-----------------------CREACION DE PESTAÑAS---------------------------------------------------------
#Crear el frame para la pestaña "Nombre"
 pestaña_nombre = ttk.Frame(notebook)
 notebook.add(pestaña_nombre, text="Nombre")
#Crear el frame para la pestaña "Tipo"
 pestaña_tipo = ttk.Frame(notebook)
 notebook.add(pestaña_tipo, text="Tipo")
 #------------------IMAGEN PARA EL FONDO(PESTAÑA NOMBRE)--------------------------------------------------------------------------------
#Cargar imagen de fondo
# Cargar y redimensionar la primera imagen
 pokedex = Image.open("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/POKEDEX.jpg")
 pokedex = pokedex.resize((550, 700), Image.Resampling.LANCZOS)
 pokedex_tk = ImageTk.PhotoImage(pokedex)
#
 pokedex2 = Image.open("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/POKEDEX3.jpg")
 pokedex2 = pokedex2.resize((550, 700), Image.Resampling.LANCZOS)
 pokedex2_tk = ImageTk.PhotoImage(pokedex2)
 
#Crear un Canvas para el fondo(PESTAÑA NOMBRE)
 canvas = tk.Canvas(pestaña_nombre, width=550, height=700)
 canvas.pack(fill="both", expand=True)
 canvas.create_image(0, 0, image=pokedex_tk, anchor="nw")
 canvas.image = pokedex_tk  #mantener referencia a la imagen
 #Crear un Canvas para el fondo(PESTAÑA TIPO)
 canvas = tk.Canvas(pestaña_tipo, width=550, height=700)
 canvas.pack(fill="both", expand=True)
 canvas.create_image(0, 0, image=pokedex2_tk, anchor="nw")
 canvas.image = pokedex2_tk  #mantener referencia a la imagen

#-----------------------APARTADO DE WIDGETS PARA LA PESTAÑA NOMBRE-----------------------
# Opciones para el menu desplegable
 opciones_busqueda = ["Busqueda ID", "Busqueda Nombre"]#opciones de momento
 tipo_busqueda = tk.StringVar()
 tipo_busqueda.set(opciones_busqueda[0]) #valor inicial del menuoption el cual sera ID
 tipo_busqueda.trace("w", lambda *args: cambiar_tipo_busqueda(tipo_busqueda, txt_busqueda_name, btn_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir))
 option_menu = tk.OptionMenu(pestaña_nombre, tipo_busqueda, *opciones_busqueda)
 option_menu.config(font=("Press Start 2P", 10), bg="green", fg="white", width=17)
 option_menu.place(x=35, y=525)
 
 
#Cuadro de texto para la búsqueda
 txt_busqueda_name = tk.Text(pestaña_nombre, font=("Press Start 2P", 13), width=12, height=1)
 txt_busqueda_name.place(x=299, y=527)

#Botón de búsqueda
 btn_busqueda_name = tk.Button(pestaña_nombre, text="BUSCAR", command=lambda:  busqueda_por_id(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir), width=7, height=2, bg="green", font=("Press Start 2P", 10))
 btn_busqueda_name.place(x=420, y=565)

#Botón para borrar/limpiar la pestaña
 btn_borrar_txt = tk.Button(pestaña_nombre, text="BORRAR", command=lambda: borrar_busqueda_name(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir), width=7, height=2, bg="red", font=("Press Start 2P", 10))
 btn_borrar_txt.place(x=420, y=615)
 
 
 frame_info_izq = tk.Frame(pestaña_nombre, bd=2, relief="solid")  # bd es el grosor, relief el estilo del borde
 frame_info_izq.place(x=50, y=384, width=300, height=110)  # Ajusta la posición y tamaño del Frame
 
 #Label para mostrar la información del Pokémon
 lb_pokemon_info = tk.Label(frame_info_izq, text="", font=("Press Start 2P", 10), bg="white", justify="left", anchor="nw",)
 lb_pokemon_info.pack(fill="both", expand=True, padx=5, pady=5)#se usa pack para que quede dentro del frame asi no se tiene que ajustar las coordenadas
 
 #Label para mostrar especificamente el tipo 
  #tipo1
 lb_pokemon_tipo1 = tk.Label(pestaña_nombre)
 lb_pokemon_tipo1.place(x=180,y=580)
 #tipo2
 lb_pokemon_tipo2 = tk.Label(pestaña_nombre)
 lb_pokemon_tipo2.place(x=300, y=580)
 #Label para mostrar el sprite(gif) del Pokémon
 lb_sprite = tk.Label(pestaña_nombre)
 lb_sprite.place(x=135, y=125) 
 
 # Crear el botón en la pestaña
 btn_reproducir = tk.Button(pestaña_nombre, text="Reproducir\nsonido", width=11, height=2, bg="blue", font=("Press Start 2P", 10))
 btn_reproducir.place(x=350, y=445)

 
 
 
#-----------------------APARTADO DE WIDGETS PARA LA PESTAÑA TIPO--------------------------------------------------------------------------------------------------

#NOTA : ACTUALMENTE LA PESTAÑA TIPO NO SE ENCUENTRA FUNCIONAL POR EL CAMBIO EN LA BASE DE DATOS

#menuoption desplegable para seleccionar el tipo
#lista de tipos pokemon (18 en total)
 tipos_pokemon = ["Todos", "Bicho", "Siniestro", "Dragón", "Eléctrico", "Hada", "Lucha", "Fuego", "Volador", "Fantasma", "Planta", "Tierra", "Hielo", "Normal", "Veneno", "Psíquico", "Roca", "Acero", "Agua"]

#variable para almacenar el tipo seleccionado
 tipo_seleccionado = tk.StringVar(value=tipos_pokemon[0])  # Selección inicial: primer tipo de la lista
 #asocia el callback al cambio de selección de tipo
 tipo_seleccionado.trace("w", lambda *args: filtrar_por_tipo_auto(tipo_seleccionado, listbox_resultados_tipo))

#menuoption para elegir el tipo
 menu_tipos = tk.OptionMenu(pestaña_tipo, tipo_seleccionado, *tipos_pokemon)
 menu_tipos.config(font=("Press Start 2P", 12), bg="green", width=12)
 menu_tipos.place(x=40, y=520)

#frame que incluira el listbox y el scrollbar
 frame_listbox_tipo = tk.Frame(pestaña_tipo)
 frame_listbox_tipo.place(x=50, y=120, width=450, height=380)

# Scrollbar
 scrollbar_tipo = tk.Scrollbar(frame_listbox_tipo)
 scrollbar_tipo.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox
 listbox_resultados_tipo = tk.Listbox(frame_listbox_tipo, yscrollcommand=scrollbar_tipo.set, font=("Press Start 2P", 10),bg="black", fg="white", width=35, height=20)
 listbox_resultados_tipo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Asociar la barra de desplazamiento al Listbox
 scrollbar_tipo.config(command=listbox_resultados_tipo.yview)
 #Evento de selección del Listbox
 listbox_resultados_tipo.bind("<<ListboxSelect>>", lambda event: mostrar_detalles_pokemon(event, listbox_resultados_tipo))
 
 #boton para actualizar la base de datos (luego de agregar un pokemon)
 btn_actualizar = tk.Button(pestaña_tipo, text="Actualizar", command=lambda: actualizar_datos(listbox_resultados_tipo), font=("Press Start 2P", 10), bg="blue", fg="white", width=11,height=2)
 btn_actualizar.place(x=250, y=50)  # Ajusta la posición según el diseño



# Botón para borrar los resultados
 btn_borrar_tipo = tk.Button(pestaña_tipo, text="BORRAR", command=lambda: listbox_resultados_tipo.delete(0, tk.END), width=7, height=2, bg="red", font=("Press Start 2P", 10))
 btn_borrar_tipo.place(x=415, y=556)
 #retono en notebook para no perder referencia
 
 #Boton de agregar un nuevo pokemon a la pokedex
 btn_agregar_pokemon = tk.Button(pestaña_tipo,text="Agregar Pokémon", command = abrir_ventana_agregar_pokemon, width=15, height=2, bg="blue", font=("Press Start 2P", 10))
 btn_agregar_pokemon.place(x=190, y=590)  # Ajusta las coordenadas según tu diseño

 return notebook

