import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="172.23.128.1", #Cambiar por la ip
        user="admin",  # Cambiar por el usuario de la base de datos
        passwd="",     
        database="pparcial"
    )
    return conexion
