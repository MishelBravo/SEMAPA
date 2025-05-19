from flask import Flask, request, jsonify, render_template, redirect
from markupsafe import Markup  # ✅ Markup se importa desde markupsafe, no flask
import folium
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime, timedelta
import time
# from cassandra.cluster import Cluster  # ← Descomenta si lo vas a usar

app = Flask(__name__)

def conectar_db():
    try:
        print("Intentando conectar a la base de datos (simulado)...")
        raise Exception("No se puede conectar (modo interfaz)")
    except Exception as e:
        print("⚠️ No se pudo conectar a la base de datos:", e)
        return None


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
