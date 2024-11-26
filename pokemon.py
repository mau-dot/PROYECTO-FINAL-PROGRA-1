from PIL import Image, ImageTk
import os
#CLASE POKEMON QUE SIRVE COMO MOLDE PARA BUSCAR A LOS POKEMONES Y SUS DATOS EN LA BASE DE DATOS
class Pokemon:
    def __init__(self, id_pokedex, nombre_pokemon, tipo1, tipo2, estatura, peso, gif, grito):
        self.id_pokedex = id_pokedex
        self.nombre = nombre_pokemon
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.estatura = estatura
        self.peso = peso
        #Normaliza la ruta generada por os.path.join. (asegura que las barras sean correctas segun el sistema operativo)
        self.gif = os.path.normpath(os.path.join("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/filtered_gifs", gif))
        #En estecaso no esta normalizada pero la busqueda es compatible con el sistema operativo
        self.grito = os.path.join("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/cries", grito)

#No se porque tengo el metodo
#pero si lo quito no funciona XD
    def __str__(self):
        return (f"ID: {self.id_pokedex}\nNombre: {self.nombre}\nTipo 1: {self.tipo1}\nTipo 2: {self.tipo2}\n"
                f"Estatura: {self.estatura}\nPeso: {self.peso}\nFoto: {self.gif}")

    #metodo para cargar y mostrar el sprite (gif) del pokemon
    #el parametro label sera donde se mostrara el gif, parametro size es la tupla encargada de estandarizar el tamaño
    def cargar_gif(self, label, size=(250, 250)):
    #manejo de exepciones con try
     try:
        #se abre la imagen que es el primer frame del gif, self.gif contiene la ruta del pokemon cuandoo se crea la instancia
        gif = Image.open(self.gif)
        #funcion interna que controla los frames del gif de manera secuencial
        def actualizar_frame(ind):
            #manejo de error por el uso de gifs que tienen que ser refrescados para mostrar cada frame en pantalla
            #algunos GIFs requieren un refresco explicito para mostrar correctamente cada cuadro, lo cual puede generar un EOFError si se intenta acceder a un cuadro inexistente.
            try:
                #ind es el indice de cuadro del gif (el gif se compone de varios cuadros o frames)
                gif.seek(ind)
                #Redimensionar el cuadro actual
                #gif.copy():crea una copia del cuadro actual para trabajar con el sin modificar el gif original
                #resize(size, Image.Resampling.LANCZOS):redimensiona el cuadro al tamaño especificado en el parametro size
                #Image.Resampling.LANCZOS: es un algoritmo de alta calidad para redimensionar imagenes
                #ImageTk.PhotoImage(frame): sonvierte el cuadro redimensionado en un formato compatible con Tkinter

                frame = gif.copy().resize(size, Image.Resampling.LANCZOS)
                frame = ImageTk.PhotoImage(frame)
                #se configura el label para que tenga como parametros el frame del gif
                label.config(image=frame)
                label.image = frame
                
                ind += 1#se avanza al siguiente cuadro (frame)
                
                if ind == gif.n_frames:#retorna el numero total de frames
                    ind = 0#al llegar al ultimo frame, el indice se reinicia a 0 para repetir el bucle
                    
                #cancela las animaciones que se muestren
                label.after_id = label.after(100, actualizar_frame, ind)#la ejecucion actualizar_frame despues de 100 milisigundos
            except EOFError:                                            #crea el efecto de animacion
                pass

        actualizar_frame(0)#inicia la animacion llamando a actualizar_frame con indice 0 (primer frame)
     except Exception as e:
        print(f"Error al cargar el GIF: {e}")
