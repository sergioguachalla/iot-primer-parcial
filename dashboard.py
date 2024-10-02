from flask import Flask, render_template, jsonify
import mysql.connector
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime
from connection import conectar

# Inicializar la aplicación Flask
app = Flask(__name__)

# Función para conectar a la base de datos
#def conectar():
#    conexion = mysql.connector.connect(
#        host="localhost",
#        user="laura",  # Cambia por tu usuario
#        password="",  # Cambia por tu contraseña
#        database="pparcial"
#    )
#    return conexion

# Función para obtener los datos de las series trigonométricas por usuario
def obtener_datos_usuario():
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT u.username, 
           st1.valor_real, st1.valor_aproximado, st1.error, 
           st2.valor_real, st2.valor_aproximado, st2.error, 
           st3.valor_real, st3.valor_aproximado, st3.error
    FROM usuarios u
    LEFT JOIN serie_trig_1 st1 ON u.id = st1.usuario_id
    LEFT JOIN serie_trig_2 st2 ON u.id = st2.usuario_id
    LEFT JOIN serie_trig_3 st3 ON u.id = st3.usuario_id
    ORDER BY u.username;
    """
    cursor.execute(sql)
    resultados = cursor.fetchall()

    datos = {
        "usuarios": [],
        "seno": {"valor_real": [], "valor_aproximado": [], "error": []},
        "coseno": {"valor_real": [], "valor_aproximado": [], "error": []},
        "fourier": {"valor_real": [], "valor_aproximado": [], "error": []},
    }

    for fila in resultados:
        datos["usuarios"].append(fila[0])  # username
        # Seno
        datos["seno"]["valor_real"].append(fila[1])
        datos["seno"]["valor_aproximado"].append(fila[2])
        datos["seno"]["error"].append(fila[3])
        # Coseno
        datos["coseno"]["valor_real"].append(fila[4])
        datos["coseno"]["valor_aproximado"].append(fila[5])
        datos["coseno"]["error"].append(fila[6])
        # Fourier
        datos["fourier"]["valor_real"].append(fila[7])
        datos["fourier"]["valor_aproximado"].append(fila[8])
        datos["fourier"]["error"].append(fila[9])

    cursor.close()
    conexion.close()

    return datos

# Ruta principal que carga el dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para actualizar los datos del gráfico
@app.route('/datos_grafico', methods=['GET'])
def datos_grafico():
    datos = obtener_datos_usuario()

    # Crear la gráfica usando Plotly
    trace1 = go.Scatter(x=datos["usuarios"], y=datos["seno"]["valor_real"], mode='lines+markers', name='Seno Real')
    trace2 = go.Scatter(x=datos["usuarios"], y=datos["seno"]["valor_aproximado"], mode='lines+markers', name='Seno Aproximado')
    trace3 = go.Scatter(x=datos["usuarios"], y=datos["seno"]["error"], mode='lines', name='Error Seno', line=dict(color='red', dash='dash'))

    trace4 = go.Scatter(x=datos["usuarios"], y=datos["coseno"]["valor_real"], mode='lines+markers', name='Coseno Real')
    trace5 = go.Scatter(x=datos["usuarios"], y=datos["coseno"]["valor_aproximado"], mode='lines+markers', name='Coseno Aproximado')
    trace6 = go.Scatter(x=datos["usuarios"], y=datos["coseno"]["error"], mode='lines', name='Error Coseno', line=dict(color='blue', dash='dash'))

    trace7 = go.Scatter(x=datos["usuarios"], y=datos["fourier"]["valor_real"], mode='lines+markers', name='fourier Real')
    trace8 = go.Scatter(x=datos["usuarios"], y=datos["fourier"]["valor_aproximado"], mode='lines+markers', name='fourier Aproximado')
    trace9 = go.Scatter(x=datos["usuarios"], y=datos["fourier"]["error"], mode='lines', name='Error fourier', line=dict(color='green', dash='dash'))

    # Combinamos todos los gráficos en uno solo
    layout = go.Layout(
        title=f'Gráfico de series trigonométricas por usuario - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        xaxis_title='Usuarios',
        yaxis_title='Valores de la serie',
        legend=dict(x=0, y=1),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9], layout=layout)

    # Convertir la gráfica a JSON para que pueda ser consumida por el frontend
    graph_json = pio.to_json(fig)

    return jsonify(graph_json)

# Función para iniciar el servidor del dashboard
def iniciar_dashboard():
    app.run(debug=True, use_reloader=False)

# Si quieres iniciar el dashboard desde un archivo separado, puedes hacer lo siguiente:
if __name__ == "__main__":
    iniciar_dashboard()
