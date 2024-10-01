import math
import random
import getpass
from connection import conectar  # Importa la función conectar desde connection.py

# Función para registrar un usuario
def registrar_usuario():
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
    conexion = conectar()
    cursor = conexion.cursor()
    username = input("Ingrese nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    sql = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    valores = (username, password)
    cursor.execute(sql, valores)
    usuario = cursor.fetchone()

    if usuario:
        print(f"Bienvenido, {username}!")
        return True
    else:
        print("Credenciales incorrectas.")
        return False

# Función para aproximar el valor del seno usando la serie de Taylor
def aproximar_seno(x, n_terminos):
    seno_aproximado = 0
    for n in range(n_terminos):
        coeficiente = (-1)**n
        numerador = x**(2*n + 1)
        denominador = math.factorial(2*n + 1)
        seno_aproximado += coeficiente * (numerador / denominador)
    return seno_aproximado

# Función para aproximar el valor del coseno usando la serie de Taylor
def aproximar_coseno(x, n_terminos):
    coseno_aproximado = 0
    for n in range(n_terminos):
        coeficiente = (-1)**n
        numerador = x**(2*n)
        denominador = math.factorial(2*n)
        coseno_aproximado += coeficiente * (numerador / denominador)
    return coseno_aproximado


# Función para insertar datos de aproximaciones trigonométricas
def insertar_aproximaciones_trig(tabla, funcion_real, funcion_aproximada, num_terminos):
    conexion = conectar()
    cursor = conexion.cursor()

    for i in range(1, num_terminos + 1):
        x = random.uniform(0, 2 * math.pi)  # Ángulo en radianes aleatorio entre 0 y 2π
        valor_real = funcion_real(x)  # Calcula el valor real usando la función matemática de Python
        valor_aproximado = funcion_aproximada(x, 5)  # Calcula la aproximación usando 5 términos de Taylor
        error = valor_aproximado - valor_real  # Error de la aproximación

        # Inserta los valores en la tabla correspondiente
        sql = f"INSERT INTO {tabla} (valor_aproximado, valor_real, error) VALUES (%s, %s, %s)"
        valores = (valor_aproximado, valor_real, error)
        cursor.execute(sql, valores)
        conexion.commit()

    print(f"Valores insertados en {tabla}.")
    cursor.close()
    conexion.close()

# Función para aproximar el valor de la tangente usando la serie de Taylor
def aproximar_tangente(x, n_terminos):
    tangente_aproximada = 0
    for n in range(n_terminos):
        if n == 0:
            coeficiente = 1
        elif n == 1:
            coeficiente = 1/3
        elif n == 2:
            coeficiente = 2/15
        elif n == 3:
            coeficiente = 17/315
        else:
            break
        
        tangente_aproximada += coeficiente * x**(2*n + 1)
    return tangente_aproximada

# Función para insertar datos en la tabla de tangente
def insertar_datos_tangente(num_terminos):
    insertar_aproximaciones_trig("serie_trig_3", math.tan, aproximar_tangente, num_terminos)

# Menú interactivo
def menu():
    while True:
        print("\n----- Menú -----")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Añadir datos tabla 2 (Serie Trigonométrica 1 - Seno)")
        print("4. Añadir datos tabla 3 (Serie Trigonométrica 2 - Coseno)")
        print("5. Añadir datos tabla 3 (Serie Trigonométrica 3 - Tangente)")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            if iniciar_sesion():
                print("Sesión iniciada.")
        elif opcion == "3":
            num_terminos = int(input("Ingrese el número de términos a añadir: "))
            insertar_aproximaciones_trig("serie_trig_1", math.sin, aproximar_seno, num_terminos)
        elif opcion == "4":
            num_terminos = int(input("Ingrese el número de términos a añadir: "))
            insertar_aproximaciones_trig("serie_trig_2", math.cos, aproximar_coseno, num_terminos)
        elif opcion == "5":
            num_terminos = int(input("Ingrese el número de términos a añadir: "))
            insertar_datos_tangente(num_terminos)
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente nuevamente.")

# Ejecutar el menú
if __name__ == "__main__":
    menu()
