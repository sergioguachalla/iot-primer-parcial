import math
import random
import getpass
import threading
import numpy as np
from connection import conectar  # Importa la función conectar desde connection.py
from dashboard import iniciar_dashboard
import numpy as np

# Función para registrar un usuario
def registrar_usuario():
    '''
    Esta función permite registrar un usuario en la base de datos, toma los datos de usuario
    como nombre de usuario, email y contraseña. Luego inserta los datos en la tabla usuarios.
    '''
    conexion = conectar()
    cursor = conexion.cursor()
    username = input("Ingrese nombre de usuario: ")
    email = input("Ingrese su email: ")
    password = input("Ingrese su contraseña: ")

    try:
        sql = "INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)"
        valores = (username, password, email)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Usuario registrado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.close()

# Función para iniciar sesión
def iniciar_sesion():
    '''
    Esta función permite a un usuario iniciar sesión en el sistema, solicita el nombre de usuario
    y la contraseña. Luego verifica si las credenciales son correctas consultando la base de datos.
    Si las credenciales son correctas, imprime un mensaje de bienvenida y devuelve el ID del usuario.
    '''
    conexion = conectar()
    cursor = conexion.cursor()
    username = input("Ingrese nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    sql = "SELECT id, username FROM usuarios WHERE username = %s AND password = %s"
    valores = (username, password)
    cursor.execute(sql, valores)
    usuario = cursor.fetchone()

    if usuario:
        print(f"Bienvenido, {usuario[1]}!")
        return usuario[0]  # Devolver el usuario_id
    else:
        print("Credenciales incorrectas.")
        return None

# Función para aproximar el valor del seno usando la serie de Taylor
'''
Esta función recibe un ángulo x y un número de términos n_terminos para aproximar el valor del seno 
'''
def aproximar_seno(x, n_terminos):
    seno_aproximado = 0
    for n in range(n_terminos):
        coeficiente = (-1)**n
        numerador = x**(2*n + 1)
        denominador = math.factorial(2*n + 1)
        seno_aproximado += coeficiente * (numerador / denominador)
    return seno_aproximado

# Función para aproximar el valor del coseno usando la serie de Taylor
'''
Esta función recibe un ángulo x y un número de términos n_terminos para aproximar el valor del coseno
'''
def aproximar_coseno(x, n_terminos):
    coseno_aproximado = 0
    for n in range(n_terminos):
        coeficiente = (-1)**n
        numerador = x**(2*n)
        denominador = math.factorial(2*n)
        coseno_aproximado += coeficiente * (numerador / denominador)
    return coseno_aproximado

# Función para la serie de Fourier
'''
Esta función recibe un ángulo x y un número de términos n_terminos para aproximar el valor de la tangente
'''
def insertar_valores_fourier(n, userId):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Define Fourier series parameters
        a0 = 0  # Constant term
        a_coefficients = [random.uniform(-1, 1) for _ in range(n)]  # Random a_n coefficients
        b_coefficients = [random.uniform(-1, 1) for _ in range(n)]  # Random b_n coefficients

        for i in range(1, n):  # Start loop from 1 to avoid division by zero
            # Generate a sample value using the Fourier series formula
            x = 2 * np.pi * i / n  # Use 'i' for the loop variable
            
            fourier_value = a0 / 2
            fourier_value += a_coefficients[i - 1] * np.cos(i * x)
            fourier_value += b_coefficients[i - 1] * np.sin(i * x)

            print(i, fourier_value)
            Conruido = fourier_value
            error = random.uniform(-0.1, 0.1)  # Example error term

            # SQL to insert data into regfourier
            sql = "INSERT INTO serie_trig_3 (valor_aproximado, valor_real, error, usuario_id) VALUES (%s, %s, %s, %s)"
            fourier_value_python = float(fourier_value)
            Conruido_python = float(Conruido)
            error_python = float(error)
            valores = (fourier_value_python, Conruido_python, error_python, userId)


            # Execute the query and commit
            cursor.execute(sql, valores)
            conexion.commit()

        cursor.close()
        conexion.close()

    except Exception as e:
        print(f"Error: {e}")


# Función para insertar datos de aproximaciones trigonométricas con el usuario_id
def insertar_aproximaciones_trig(tabla, funcion_real, funcion_aproximada, num_terminos, usuario_id):
    conexion = conectar()
    cursor = conexion.cursor()

    for i in range(1, num_terminos + 1):
        x = random.uniform(0, 2 * math.pi)  # Ángulo en radianes aleatorio entre 0 y 2π
        valor_real = funcion_real(x)  # Calcula el valor real usando la función matemática de Python
        valor_aproximado = funcion_aproximada(x, 5)  # Calcula la aproximación usando 5 términos de Taylor
        error = valor_aproximado - valor_real  # Error de la aproximación

        # Inserta los valores en la tabla correspondiente junto con el usuario_id
        sql = f"INSERT INTO {tabla} (valor_aproximado, valor_real, error, usuario_id) VALUES (%s, %s, %s, %s)"
        valores = (valor_aproximado, valor_real, error, usuario_id)
        cursor.execute(sql, valores)
        conexion.commit()

    print(f"Valores insertados en {tabla}.")
    cursor.close()
    conexion.close()

# Menú interactivo
def menu():
    usuario_id = None  # Variable para almacenar el ID del usuario tras iniciar sesión
    while True:
        print("\n----- Menú -----")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Añadir datos tabla 1 (Serie Trigonométrica 1 - Seno)")
        print("4. Añadir datos tabla 2 (Serie Trigonométrica 2 - Coseno)")
        print("5. Añadir datos tabla 3 (Serie Trigonométrica 3 - Fourier)")
        print("6. Dashboard")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            usuario_id = iniciar_sesion()  # Al iniciar sesión se guarda el ID del usuario
        elif opcion == "3":
            if usuario_id:
                num_terminos = int(input("Ingrese el número de términos a añadir: "))
                insertar_aproximaciones_trig("serie_trig_1", math.sin, aproximar_seno, num_terminos, usuario_id)
            else:
                print("Debes iniciar sesión primero.")
        elif opcion == "4":
            if usuario_id:
                num_terminos = int(input("Ingrese el número de términos a añadir: "))
                insertar_aproximaciones_trig("serie_trig_2", math.cos, aproximar_coseno, num_terminos, usuario_id)
            else:
                print("Debes iniciar sesión primero.")
        elif opcion == "5":
            if usuario_id:
                num_terminos = int(input("Ingrese el número de términos a añadir: "))
                insertar_valores_fourier(num_terminos,usuario_id)
            else:
                print("Debes iniciar sesión primero.")
        elif opcion == "6":
            # Ejecutar el dashboard en un hilo separado
            hilo_dashboard = threading.Thread(target=iniciar_dashboard)
            hilo_dashboard.start()
        elif opcion == "7":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente nuevamente.")

# Ejecutar el menú
if __name__ == "__main__":
    menu()
