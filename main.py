from flask import Flask, request, jsonify, render_template, redirect
from markupsafe import Markup  
import folium
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime, timedelta
import time
from cassandra.cluster import Cluster

app = Flask(__name__)

def test_cassandra_connection():
    try:
        cluster = Cluster(['127.0.0.1'])  # Cambia la IP si es necesario
        session = cluster.connect()
        session.set_keyspace('semapa')
        session.execute("SELECT release_version FROM system.local")
        print("✅ Conexión a Cassandra exitosa")
        return session
    except Exception as e:
        print(f"❌ Error al conectar a Cassandra: {e}")
        return None

# Probar conexión al iniciar la app
session = test_cassandra_connection()


# Redirigimiento a pestañas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/principal_semapa')    
def index():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/buscar')
def prueba():
    return render_template('buscar.html')

if __name__ == '__main__':
    app.run(debug=True)
