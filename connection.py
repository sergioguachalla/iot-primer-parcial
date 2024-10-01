import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost", #Cambiar por la ip
        user="laura",  # Cambiar por el usuario de la base de datos
        passwd="",     
        database="pparcial"
    )
    return conexion
