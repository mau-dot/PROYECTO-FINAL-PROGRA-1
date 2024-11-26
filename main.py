import tkinter as tk 
from notebooks import pestañas

#-----------------------APARTADO DE VENTANA PRINCIPAL---------------------------------------------------------------------------------------
#crear ventana principal
root = tk.Tk()
#icono
root.iconbitmap("C:/Users/MAUW/OneDrive/Escritorio/PROYECTO FINAL PROGRA 1/imagenes/pokeball_icon.ico")
#Titulo principal
root.title("POKÉDEX")
#Dimensiones de la pagina
root.geometry("550x700")
#
root.resizable(False, False)
#-------------------------------------------------------------------------------------------------------------------------------------------
#metodo que contiene todos las pestañas, widgets y codidigo en general
pestañas(root)
#iniciar el bucle principal de la ventana
root.mainloop()
