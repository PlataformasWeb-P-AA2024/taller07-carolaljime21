from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from genera_tablas import Club, Jugador
from configuracion import cadena_base_datos

# Crear el engine y la sesión
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Función para leer datos de un archivo
def leer_datos_club(ruta):
    clubs = []
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            nombre, deporte, fundacion = linea.strip().split(';')
            clubs.append(Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion)))
    return clubs

def leer_datos_jugador(ruta, session):
    jugadores = []
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            nombre_club, posicion, dorsal, nombre = linea.strip().split(';')
            club = session.query(Club).filter_by(nombre=nombre_club).one_or_none()
            if club is None:
                print(f"Error: No se encontró el club con nombre '{nombre_club}'")
            else:
                jugadores.append(Jugador(nombre=nombre, dorsal=int(dorsal), posicion=posicion, club=club))
    return jugadores

# Leer datos de los archivos
clubs = leer_datos_club('data/datos_clubs.txt')

# Agregar clubs a la sesión
session.add_all(clubs)

# Confirmar las transacciones para los clubs
session.commit()

# Leer y agregar jugadores
jugadores = leer_datos_jugador('data/datos_jugadores.txt', session)

# Agregar jugadores a la sesión
session.add_all(jugadores)

# Confirmar las transacciones para los jugadores
session.commit()