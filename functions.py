#Funciones para cada button, buscar, borrar etc
#importaciones desde las conecciones de la base de datos y las consultas sql
from database import get_pokemon_name, get_pokemon_tipo, get_pokemon_todos, connect_db, TIPOS_RUTAS
import tkinter as tk 
from PIL import Image, ImageTk
import pygame
from tkinter import Toplevel, messagebox, ttk
from tkinter import filedialog




#-------------------------------FUNCIONES DE BOTONES EN LA VENTANA NOMBRE----------------------------------------------------------


#funcion que cambia el comportamiento del tipo de busqueda segun el menuoption
def cambiar_tipo_busqueda(tipo_busqueda, txt_busqueda_name, btn_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir):
    #Obtener el valor seleccionado del OptionMenu
    opcion = tipo_busqueda.get()
    #Modificar el comportamiento del botón según la opción seleccionada
    if opcion == "Busqueda ID":
        btn_busqueda_name.config(command=lambda: busqueda_por_id(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir))
    elif opcion == "Busqueda Nombre":
        btn_busqueda_name.config(command=lambda: busqueda_por_nombre(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir))


#funcion que tomara el boton si el menuoption cambia a nombre
def busqueda_por_nombre(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir):
    #obtener el valor del campo de texto tk.END para asegurar que se obtenga todo el contenido, strip para no dejar espacios, capitalize es para que siempre comience con mayuscula
    entrada = txt_busqueda_name.get("1.0", tk.END).strip().capitalize()
    if entrada:  #verifica que la entrada sea valida
        #obtener el pokemon por nombre
        pokemon = get_pokemon_name(nombre_pokemon=entrada)#se llama a la funcion que obtiene las consultas sql y buscara solo por el nombre
        
        if pokemon:#si el pokemon es encontrado en el base de datos
            #mostrar información general del Pokémon
            lb_pokemon_info.config(text=f"DATA :\nID: {pokemon.id_pokedex}\nNombre: {pokemon.nombre}\nEstatura (mts): {pokemon.estatura}\nPeso (kg): {pokemon.peso}")
            #carga y muestra el tipo 1
            if pokemon.tipo1:
                #carga la imagen desde la ruta obtenida almacenada en pokemon.tipo1, y la redimenciona
                tipo1_img = Image.open(pokemon.tipo1).resize((100, 60), Image.Resampling.LANCZOS)
                tipo1_tk = ImageTk.PhotoImage(tipo1_img)#convierte la imagen a un ormato compatible para tkinter
                lb_pokemon_tipo1.config(image=tipo1_tk)#actualiza el label con la imagen 
                lb_pokemon_tipo1.image = tipo1_tk#impide que la imagen sea eliminada
            else:
                #en caso de no ser encontrado el tipo el label se configura vacioo
                lb_pokemon_tipo1.config(image="")
            
            #cargar y muestra el tipo 2 (si existe)
            if pokemon.tipo2:
                tipo2_img = Image.open(pokemon.tipo2).resize((100, 60), Image.Resampling.LANCZOS)
                tipo2_tk = ImageTk.PhotoImage(tipo2_img)
                lb_pokemon_tipo2.config(image=tipo2_tk)
                lb_pokemon_tipo2.image = tipo2_tk
            else:
                lb_pokemon_tipo2.config(image="")
            
            #mostrar el sprite del Pokémon
            pokemon.cargar_gif(lb_sprite)
            #configura el boton de sonido segun el pokemon
            btn_reproducir.config(command=lambda: reproducir_grito(pokemon.grito), state='normal')#parametro normal para que el boton pueda ser precionado 
        else:
            #de no encontrarse el pokemon todo se configura vacio, y se lanza el mensaje de pokemon no encontrado
            lb_pokemon_info.config(text="Pokémon\nno encontrado")
            lb_pokemon_tipo1.config(image="")
            lb_pokemon_tipo2.config(image="")
            lb_sprite.config(image="")
            btn_reproducir.config(command=None)#deshabilita el boton si no hay pokemon encontrado
    else:
        lb_pokemon_info.config(text="Por favor\nintroduce un nombre válido")
        btn_reproducir.config(command=None) #deshabilita rl boton si la entrada es invalida

#primera funcion que se ultilizara ya que el menuoption comienza con posicion [0]
def busqueda_por_id(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir):
    #obtener el valor del campo de texto
    entrada = txt_busqueda_name.get("1.0", tk.END).strip()
    #se valida si es un digito el que se esta ingresando
    if entrada.isdigit():
        id_pokedex = int(entrada)
        #obtener el pokemon solo por ID
        pokemon = get_pokemon_name(id_pokedex=id_pokedex)
        
        if pokemon:
            #mostrar información general del pokemon
            lb_pokemon_info.config(text=f"DATA :\nID: {pokemon.id_pokedex}\nNombre: {pokemon.nombre}\nEstatura (mts): {pokemon.estatura}\nPeso (kg): {pokemon.peso}")
            #cargar y mostrar el tipo 1
            if pokemon.tipo1:
                tipo1_img = Image.open(pokemon.tipo1).resize((100, 60), Image.Resampling.LANCZOS)
                tipo1_tk = ImageTk.PhotoImage(tipo1_img)
                lb_pokemon_tipo1.config(image=tipo1_tk)
                lb_pokemon_tipo1.image = tipo1_tk
            else:
                lb_pokemon_tipo1.config(image="")
            
            #cargar y mostrar el tipo 2 (si es que existe)
            if pokemon.tipo2:
                tipo2_img = Image.open(pokemon.tipo2).resize((100, 60), Image.Resampling.LANCZOS)
                tipo2_tk = ImageTk.PhotoImage(tipo2_img)
                lb_pokemon_tipo2.config(image=tipo2_tk)
                lb_pokemon_tipo2.image = tipo2_tk
            else:
                lb_pokemon_tipo2.config(image="")
            
            #mostrar el sprite del pokemon
            pokemon.cargar_gif(lb_sprite)
            btn_reproducir.config(command=lambda: reproducir_grito(pokemon.grito), state='normal')
        else:
            lb_pokemon_info.config(text="Pokémon\nno encontrado")
            lb_pokemon_tipo1.config(image="")
            lb_pokemon_tipo2.config(image="")
            lb_sprite.config(image="")
            btn_reproducir.config(command=None)  #deshabilita el boton si no hay pokemon encontrado
    else:
        lb_pokemon_info.config(text="Por favor\nintroduce un ID válido")
        btn_reproducir.config(command=None)  #deshabilita el boton si la entrada es incorrecta
        
#funcion que utiliza la libreria de pygame para poder cargar los audios de los pokemon
def reproducir_grito(ruta_audio):
    #manejo de excepciones en caso de no ser encontrado
    try:
        pygame.mixer.init()#se inicializa el mezclador
        pygame.mixer.music.load(ruta_audio)#cargar el archivo de audio
        pygame.mixer.music.play()#reproducir audio
    except Exception as e:
        print(f"ERROR AL REPRODUCIR AUDIO : {e}")
            

#funcion para borrar la busqueda (limpiar la pantalla)
def borrar_busqueda_name(txt_busqueda_name, lb_pokemon_info, lb_pokemon_tipo1, lb_pokemon_tipo2, lb_sprite, btn_reproducir):
     txt_busqueda_name.delete("1.0", tk.END)#delete para borrar el texto
     #se usa config() con el parametro text vacio para vaciar los label
     lb_pokemon_info.config(text="") 
     lb_pokemon_tipo1.config(image="")
     lb_pokemon_tipo2.config(image="")
     lb_sprite.config(image="")
     lb_sprite.image = None 
     lb_sprite.after_cancel(lb_sprite.after_id)#Detiene el bucle del GIF si existe
     btn_reproducir.config(command=None, state='disabled')#al borrar el boton pasa con parametro "disabled"
     #esto devido a que no se como eliminar el audio de la configuracion, y aunque limpie la pantalla el audio sigue siendo disponible, hasta que cambie de pokemon
     
#_______________________________________________________________________________________________________________________________________________    
#_______________________________________________________________________________________________________________________________________________    
#_______________________________________________________________________________________________________________________________________________    
#--------------------------------FUNCIONES PARA LA PESTAÑA TIPO-----------------------------------------------------------------

#funcion para el menuoption
def filtrar_por_tipo_auto(tipo_seleccionado, listbox_resultados_tipo):#listbo que sera introducido a un frame junto con un scrollbar
    #obtener el tipo seleccionado
    tipo = tipo_seleccionado.get()

    #limpiar el Listbox antes de agregar resultados
    listbox_resultados_tipo.delete(0, tk.END)
    #si se selecciona se llama la funcion de buscar todos los pokemon
    if tipo == "Todos":
        resultados = get_pokemon_todos()
    else:# en caso contrario se buscara segun el tipo que se seleecione en la tupla 
        resultados = get_pokemon_tipo(tipo)

    #mostrar los resultados en el Listbox
    if resultados:
        for pokemon in resultados:
            listbox_resultados_tipo.insert(tk.END, f"{pokemon.id_pokedex} - {pokemon.nombre}")
    else:
        listbox_resultados_tipo.insert(tk.END, "No se encontraron Pokémon de este tipo.")

def mostrar_detalles_pokemon(event, listbox):#event: Se usa para manejar el evento de seleccion en el Listbox. Este evento se activa al seleccionar un elemento en el Listbox.
    #obtencion del elemento seleccionado
    seleccion = listbox.curselection()
    #si no se selecciono nada, la función termina (return).
    if not seleccion:
        return

    #obtiene el texto del elemento seleccionado usando el indice proporcionado por curselection()
    seleccionado = listbox.get(seleccion[0])
    
    #obtiene el ID del Pokémon
    id_pokedex = seleccionado.split("-")[0].strip()  #elimina espacios adicionales
    print(f"ID seleccionado: {id_pokedex}")  #depuración

    #obtener los datos del pokemon de la base de datos
    pokemon = get_pokemon_name(id_pokedex=id_pokedex)  #se llama la funcion que  busque solo por parametro id(se puede hacer tambien mediante nombre)
    
    if not pokemon:# en caso de no encontrase el pokemon
        #depuracion en consola y mensaje al usuario
        print(f"No se encontraron datos para el ID: {id_pokedex}")  # Depuración
        messagebox.showerror("Error", f"No se encontraron datos para el ID {id_pokedex}.")
        return  #salir si no se encuentran datos

    #Crear una nueva ventana para mostrar los detalles
    ventana_detalles = Toplevel()
    #se agrega el icono
    ventana_detalles.iconbitmap("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/pokeball_icon.ico")
    #su titulo
    ventana_detalles.title(f"DATA de {pokemon.nombre} (vista rapida)")
    #la dimesion de la ventana
    ventana_detalles.geometry("465x465")
    
    #esto para que no se agrande y no se pegue alto bug
    ventana_detalles.resizable(False, False)
    #abrir el fondo de la ventana emergente
    fondo = Image.open("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/fondo21.png")
    fondo = fondo.resize((465, 465), Image.Resampling.LANCZOS)
    fondo_tk = ImageTk.PhotoImage(fondo)
    #canvas para el fondo de la ventana
    canvas = tk.Canvas(ventana_detalles, width=550, height=700)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")
    canvas.image = fondo_tk  #mantener referencia a la imagen

    # Mostrar informacion general del pokemon
    lbl_info = tk.Label(ventana_detalles,text=(f"ID: {pokemon.id_pokedex}\n"f"Nombre: {pokemon.nombre}\n" f"Estatura (mts): {pokemon.estatura}\n" f"Peso (kg): {pokemon.peso}"),font=("Press Start 2P", 12), justify=tk.LEFT)
    lbl_info.place(x=80, y=20)
    # se muestran los tipos
    if pokemon.tipo1:
        tipo1_img = Image.open(pokemon.tipo1).resize((100, 60), Image.Resampling.LANCZOS)
        tipo1_tk = ImageTk.PhotoImage(tipo1_img)
        lb_pokemon_tipo1=tk.Label(ventana_detalles)
        lb_pokemon_tipo1.config(image=tipo1_tk)
        lb_pokemon_tipo1.image = tipo1_tk
        lb_pokemon_tipo1.place(x=80, y=330)

    else:
        lb_pokemon_tipo1.config(image="")     
        #cargar y mostrar el tipo 2 (si es que existe)
    if pokemon.tipo2:
        tipo2_img = Image.open(pokemon.tipo2).resize((100, 60), Image.Resampling.LANCZOS)
        tipo2_tk = ImageTk.PhotoImage(tipo2_img)
        lb_pokemon_tipo2=tk.Label(ventana_detalles)
        lb_pokemon_tipo2.config(image=tipo2_tk)
        lb_pokemon_tipo2.image = tipo2_tk
        lb_pokemon_tipo2.place(x=250, y=330)
    

    # Mostrar el GIF del pokemon si existe
    if pokemon.gif:
        try:
            img = Image.open(pokemon.gif).resize((150, 150), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            lbl_gif = tk.Label(ventana_detalles, image=img_tk)
            lbl_gif.image = img_tk  #mantener referencia
            lbl_gif.place(x=150, y=150)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")  #depuracion
            tk.Label(ventana_detalles, text="No se pudo cargar la imagen.", font=("Press Start 2P", 10)).place(x=150, y=150)

    # Boton para cerrar la ventana
    btn_cerrar = tk.Button(ventana_detalles, text="Cerrar", command=ventana_detalles.destroy, font=("Press Start 2P", 10))
    btn_cerrar.place(x=200, y=430)



#lista de los tipos 
TIPOS = [
"Bicho", "Siniestro", "Dragón", "Eléctrico", "Hada", "Lucha", "Fuego", "Volador",
"Fantasma", "Planta", "Tierra", "Hielo", "Normal", "Veneno", "Psíquico", "Roca",
"Acero", "Agua"
]


#funcion para abrir la ventana del apartado de agregar pokemon
def abrir_ventana_agregar_pokemon():
    # Crear una ventana secundaria
    ventana_agregar = Toplevel()
    ventana_agregar.iconbitmap("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/pokeball_icon.ico")
    ventana_agregar.title("¡Agrega tu Pokémon!")
    ventana_agregar.geometry("520x690")
    ventana_agregar.resizable(False, False)
    #cargar imagen para agregar pokemon
    pokedex_agregar = Image.open("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/fondo22.jpg")
    pokedex_agregar = pokedex_agregar.resize((520, 690), Image.Resampling.LANCZOS)
    pokedex_agregar_tk = ImageTk.PhotoImage(pokedex_agregar)
    #canvas del fondo
    canvas = tk.Canvas(ventana_agregar, width=520, height=690)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=pokedex_agregar_tk, anchor="nw")
    canvas.image = pokedex_agregar_tk  #mantener referencia a la imagen


    # Campos del formulario
    tk.Label(ventana_agregar, text="ID :", font=("Press Start 2P", 12)).place(x=60, y=60)
    entry_id = tk.Entry(ventana_agregar, font=("Press Start 2P", 12), width=6)
    entry_id.place(x=135, y=60)

    tk.Label(ventana_agregar, text="Nombre :", font=("Press Start 2P", 12)).place(x=60, y=120)
    entry_nombre = tk.Entry(ventana_agregar, font=("Press Start 2P", 12), width=10)
    entry_nombre.place(x=200, y=120)

    tk.Label(ventana_agregar, text="Estatura :", font=("Press Start 2P", 12)).place(x=60, y=170)
    entry_estatura = tk.Entry(ventana_agregar, font=("Press Start 2P", 12), width=6)
    entry_estatura.place(x=230, y=170)

    tk.Label(ventana_agregar, text="Peso :", font=("Press Start 2P", 12)).place(x=60, y=230)
    entry_peso = tk.Entry(ventana_agregar, font=("Press Start 2P", 12), width=6)
    entry_peso.place(x=180, y=230)

    # Ruta del GIF
    tk.Label(ventana_agregar, text="GIF :", font=("Press Start 2P", 12)).place(x=60, y=300)
    entry_gif = tk.Entry(ventana_agregar, font=("Press Start 2P", 12), width=10)
    entry_gif.place(x=200, y=300)

    btn_explorar_gif = tk.Button(ventana_agregar, text="Explorar", command=lambda: seleccionar_archivo(entry_gif), font=("Press Start 2P", 10))
    btn_explorar_gif.place(x=380, y=300)
    

    # Ruta del sonido
    tk.Label(ventana_agregar, text="Sonido :", font=("Press Start 2P", 12)).place(x=60, y=350)
    entry_grito = tk.Entry(ventana_agregar, font=("Press Start 2P", 12), width=10)
    entry_grito.place(x=200, y=350)

    btn_explorar_grito = tk.Button(ventana_agregar, text="Explorar", command=lambda: seleccionar_archivo(entry_grito), font=("Press Start 2P", 10))
    btn_explorar_grito.place(x=380, y=350)
    
    #seleccion de tipo 1 y 2 con combobox
    # Selección de Tipo 1
    tk.Label(ventana_agregar, text="Tipo 1", font=("Press Start 2P", 12)).place(x=60, y=400)
    combo_tipo1 = ttk.Combobox(ventana_agregar, values=TIPOS, font=("Press Start 2P", 10), state="readonly", width=10)
    combo_tipo1.place(x=180, y=400)

    # Selección de Tipo 2
    tk.Label(ventana_agregar, text="Tipo 2 (opcional)", font=("Press Start 2P", 12)).place(x=60, y=470)
    combo_tipo2 = ttk.Combobox(ventana_agregar, values=TIPOS, font=("Press Start 2P", 10), state="readonly", width=10)
    combo_tipo2.place(x=350, y=470)
    

    # Botón para guardar
    btn_guardar = tk.Button(
        ventana_agregar,
        text="Guardar",
        command=lambda: guardar_pokemon(
            entry_id.get(),
            entry_nombre.get(),
            combo_tipo1.get(),
            combo_tipo2.get(),
            entry_estatura.get(),
            entry_peso.get(),
            entry_gif.get(),
            entry_grito.get(),
            ventana_agregar
        ),
        bg="green",
        font=("Press Start 2P", 12)
    )
    btn_guardar.place(x=180, y=600)


def seleccionar_archivo(entry):
    #Abre el explorador de archivos y coloca la ruta seleccionada en el Entry correspondiente
    # se especifican los archivos compatibles etc
    ruta_archivo = filedialog.askopenfilename( title="Seleccionar archivo",filetypes=(("Archivos compatibles", "*.gif;*.mp3;*.wav"), ("Todos los archivos", "*.*")))
    if ruta_archivo:
        entry.delete(0, tk.END)  # Borra cualquier texto previo
        entry.insert(0, ruta_archivo)  # Inserta la ruta seleccionada




#funcion que guarda el pokemon creado
def guardar_pokemon(id_pokedex, nombre, tipo1, tipo2, estatura, peso, gif, grito, ventana):
    #manejo de errores en caso de agregar un dato de manera incorrecta
    try:
        #validacion de datos mediante messagebox
        if not id_pokedex.isdigit():# si el dato ingresado no es un digito en el campo id
            messagebox.showerror("Error", "El ID debe ser un número.")
            return
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")#mismo caso en el texto
            return
        if not tipo1:#obligatoriamente se tiene que seleccionar el tipo 1
            messagebox.showerror("Error", "El tipo 1 es obligatorio.")
            return
        if not estatura.replace(".", "", 1).isdigit() or not peso.replace(".", "", 1).isdigit():
            messagebox.showerror("Error", "Estatura y peso deben ser números válidos.")
            return

        #obtener las rutas de los tipos seleccionados
        tipo1_ruta = TIPOS_RUTAS.get(tipo1, "")  # Busca la ruta del tipo 1
        tipo2_ruta = TIPOS_RUTAS.get(tipo2, "") if tipo2 else None  # Busca la ruta del tipo 2, si existe

        #validar que las rutas sean correctas
        if not tipo1_ruta:
            messagebox.showerror("Error", f"No se encontró un sprite para el tipo: {tipo1}")
            return
        if tipo2 and not tipo2_ruta:
            messagebox.showerror("Error", f"No se encontró un sprite para el tipo: {tipo2}")
            return

        #conexion a la base de datos e insercion mediante consulta sql
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Quinta_Generacion (id_pokedex, nombre_pokemon, tipo1, tipo2, estatura, peso, gif, grito)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id_pokedex, nombre, tipo1_ruta, tipo2_ruta, float(estatura), float(peso), gif, grito))

        conn.commit()
        conn.close()#pa cerrar

        #confirmacion y cierre de la ventana
        messagebox.showinfo("Éxito", f"¡El Pokémon {nombre} fue agregado correctamente!")
        ventana.destroy()
    except Exception as e:
        print(f"Error al guardar el Pokémon: {e}")
        messagebox.showerror("Error", "Ocurrió un error al guardar el Pokémon.")

#funcion para actualizar el frame en la pestaña tipo(un poco innecesario)
def actualizar_datos(listbox):
    try:
        #Limpiar el Listbox
        listbox.delete(0, tk.END)

        #Conectar a la base de datos y obtener todos los pokemon
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id_pokedex, nombre_pokemon
            FROM Quinta_Generacion
            ORDER BY id_pokedex ASC
        ''')
        pokemon_lista = cursor.fetchall()
        conn.close()

        # Agregar los datos al Listbox
        for pokemon in pokemon_lista:
            id_pokedex, nombre = pokemon
            texto = f"{id_pokedex} - {nombre} "
            listbox.insert(tk.END, texto)
    except Exception as e:
        print(f"Error al actualizar los datos: {e}")
        messagebox.showerror("Error", "No se pudieron actualizar los datos.")
