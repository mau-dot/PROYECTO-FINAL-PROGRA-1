import sqlite3
from pokemon import Pokemon

#DIGANLE A IKER QUE PASE BIEN LAS RUTAS ;(

#conexion con la base de datos
def connect_db():
    return sqlite3.connect("pokemon_data.db")

#diccionario con las rutas de los tipos, r para evitar errores con las barras (creo que me daba error si las invertia)
TIPOS_RUTAS = {
    "Bicho": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Bicho.png",
    "Siniestro": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Siniestro.png",
    "Dragón": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Dragón.png",
    "Eléctrico": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Eléctrico.png",
    "Hada": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Hada.png",
    "Lucha": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Lucha.png",
    "Fuego": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Fuego.png",
    "Volador": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Volador.png",
    "Fantasma": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Fantasma.png",
    "Planta": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Planta.png",
    "Tierra": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Tierra.png",
    "Hielo": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Hielo.png",
    "Normal": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Normal.png",
    "Veneno": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Veneno.png",
    "Psíquico": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Psíquico.png",
    "Roca": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Roca.png",
    "Acero": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Acero.png",
    "Agua": r"C:\Users\MAUW\OneDrive\Escritorio\PROYECTO FINAL PROGRA 1\tipos\Agua.png"
}



#-----------------------FUNCIONES PARA PESTAÑA NOMBRE-----------------------------------------------

#obtener pokemon por nombre o por id
def get_pokemon_name(nombre_pokemon=None, id_pokedex=None):
  conn = connect_db()
  cursor = conn.cursor()
#si es por nombre
  if nombre_pokemon:
    #de momento especifico los campos ya que la base de datos sera modificada, esto conel fin de evitar errores
    cursor.execute('''                
        SELECT id_pokedex, nombre_pokemon, tipo1, tipo2, estatura, peso, gif, grito
        FROM Quinta_Generacion WHERE nombre_pokemon = ?
    ''', (nombre_pokemon,))
#si es por su id en la base de datos 
  elif id_pokedex is not None:# is not None es para que tome el 0 como digito y no como False (no realiza la busqueda si no se aclara eso )
    cursor.execute('''
        SELECT id_pokedex, nombre_pokemon, tipo1, tipo2, estatura, peso, gif, grito
        FROM Quinta_Generacion WHERE id_pokedex = ?
    ''', (id_pokedex,))
#en caso de no ser ninguno de los dos 
  else:
        #si no se proporciona ni nombre ni ID, retornar None
        conn.close()
        return None
    
  row = cursor.fetchone()
  conn.close()
  if row:
        return Pokemon(*row)
  return None


#---------------------------------FUNCIONES PARAPESTAÑA TIPO-----------------------------
def get_pokemon_tipo(tipo):
    from database import TIPOS_RUTAS
    conn = connect_db()
    cursor = conn.cursor()

    #Convertir el tipo seleccionado a su ruta correspondiente
    tipo_ruta = TIPOS_RUTAS.get(tipo)

    if not tipo_ruta:
        print("El tipo seleccionado no tiene una ruta válida.")
        conn.close()
        return []

   #consulta sql
    query = '''
        SELECT id_pokedex, nombre_pokemon, tipo1, tipo2, estatura, peso, gif, grito
        FROM Quinta_Generacion
        WHERE tipo1 = ? OR tipo2 = ?
    '''
    # Ejecutar la consulta
    cursor.execute(query, (tipo_ruta, tipo_ruta))
    rows = cursor.fetchall()

    conn.close()#cerrao

    #crear objetos pokemon si se encontraron resultados
    #rows es el resultado de una consulta SQL ejecutada con un cursor de SQLite

    if rows:#verifica si se obtuvieron resultados
        #si se encuentran los resultados segun su tipo se crea una lista comprensible con los resultados
        pokemones = [Pokemon(*row) for row in rows]
        return pokemones
    #Si no hay resultados retornara una lista vacia
    return []




#funcion para buscar todos los pokemon
def get_pokemon_todos():
    conn = connect_db()
    cursor = conn.cursor()

    # Consulta SQL para obtener todos los Pokémon
    cursor.execute('''
        SELECT id_pokedex, nombre_pokemon, tipo1, tipo2, estatura, peso, gif, grito
        FROM Quinta_Generacion
    ''')

    rows = cursor.fetchall()
    conn.close()

    #crear objetos pokemon si se encontraron resultados
    if rows:
        pokemones = [Pokemon(*row) for row in rows]
        return pokemones
    return []
