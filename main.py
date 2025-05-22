from flask import Flask, request, jsonify, render_template, redirect
from markupsafe import Markup  
import folium
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime, timedelta
import time
from cassandra.cluster import Cluster

app = Flask(__name__)

def get_session():
    try:
        cluster = Cluster(['127.0.0.1'])  # Cambia la IP si es necesario
        session = cluster.connect()
        session.set_keyspace('semapados')
        session.execute("SELECT release_version FROM system.local")
        print("✅ Conexión a Cassandra exitosa")
        return session
    except Exception as e:
        print(f"❌ Error al conectar a Cassandra: {e}")
        return None

# Probar conexión al iniciar la app
session = get_session()

#_---------------------------------------------------------------------------------------------------------
def consulta_factura(numero_contrato=None, nombre_usuario=None, fecha_string=None):
    session = get_session()

    try:
        if not fecha_string:
            return {"error": "Fecha inválida."}

        fecha = datetime.strptime(fecha_string, "%Y-%m-%d")
        contrato = None

        if nombre_usuario:
            usuario = session.execute("""
                SELECT idUsuario FROM Usuario WHERE nombre = %s ALLOW FILTERING
            """, [nombre_usuario]).one()

            if not usuario:
                return {"error": "Usuario no encontrado."}

            id_usuario = usuario.idusuario

            if numero_contrato:
                contrato = session.execute("""
                    SELECT * FROM ContratoMedidor 
                    WHERE numeroContrato = %s AND fk_idUsuario = %s ALLOW FILTERING
                """, [numero_contrato, id_usuario]).one()
            else:
                contrato = session.execute("""
                    SELECT * FROM ContratoMedidor 
                    WHERE fk_idUsuario = %s ALLOW FILTERING
                """, [id_usuario]).one()
        elif numero_contrato:
            contrato = session.execute("""
                SELECT * FROM ContratoMedidor 
                WHERE numeroContrato = %s ALLOW FILTERING
            """, [numero_contrato]).one()

        if not contrato:
            return {"error": "Contrato no encontrado."}

        id_usuario = contrato.fk_idusuario
        id_infraestructura = contrato.fk_idinfraestructura
        mac_medidor = contrato.macmedidor

        usuario = session.execute("""
            SELECT * FROM Usuario WHERE idUsuario = %s
        """, [id_usuario]).one()

        infraestructura = session.execute("""
            SELECT tipoInfraestructura, fk_idTarifario 
            FROM Infraestructura 
            WHERE idInfraestructura = %s
        """, [id_infraestructura]).one()

        tarifario = None
        if infraestructura:
            tarifario = session.execute("""
                SELECT * FROM Tarifario 
                WHERE idTarifario = %s
            """, [infraestructura.fk_idtarifario]).one()

        fecha_inicio = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
        fecha_fin = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)

        lecturas = session.execute("""
            SELECT fechaMedidor, consumo, macMedidor 
            FROM LecturaMedidor 
            WHERE macMedidor = %s ALLOW FILTERING
        """, [mac_medidor])

        lecturas_filtradas = [
            {
                "fechaMedidor": l.fechamedidor.isoformat(),
                "consumo": l.consumo,
                "macMedidor": l.macmedidor
            }
            for l in lecturas if fecha_inicio <= l.fechamedidor <= fecha_fin
        ]

        resultado = {
            "numeroContrato": contrato.numerocontrato,
            "fechaInstalacion": contrato.fechainstalacion.isoformat() if contrato.fechainstalacion else None,
            "usuario": {
                "idUsuario": str(usuario.idusuario),
                "nombre": usuario.nombre,
                "correoElectronico": usuario.correoelectronico,
                "telefono": usuario.telefono,
                "tipopersona": usuario.tipopersona
            } if usuario else None,
            "infraestructura": {
                "tipoInfraestructura": infraestructura.tipoinfraestructura
            } if infraestructura else None,
            "tarifario": {
                "nombre": tarifario.nombre,
                "tipo": tarifario.tipotarifario,
                "m3Mes": tarifario.m3mes,
                "usMes": tarifario.usmes
            } if tarifario else None,
            "lecturas": lecturas_filtradas
        }

        print("✅ Consulta exitosa, devolviendo resultado.")
        return resultado

    except Exception as e:
        print(f"❌ Error interno en consulta_factura: {str(e)}")
        return {"error": "Error al procesar la solicitud."}

    finally:
        session.shutdown()


@app.route('/consulta_factura', methods=['POST'])
def consulta_factura_endpoint():
    try:
        data = request.get_json()

        numero_contrato = data.get('numero_contrato')
        nombre_usuario = data.get('nombre_usuario')
        fecha_medidor = data.get('fecha')

        print("📥 Datos recibidos en endpoint:")
        print(f"numero_contrato: {numero_contrato}")
        print(f"nombre_usuario: {nombre_usuario}")
        print(f"fecha_medidor: {fecha_medidor}")

        resultado = consulta_factura(numero_contrato, nombre_usuario, fecha_medidor)

        # Si el resultado contiene un error, lo devolvemos como tal
        if "error" in resultado:
            return jsonify({"status": "error", "message": resultado["error"]}), 400

        return jsonify({
            "status": "success",
            "data": resultado
        })

    except Exception as e:
        print(f"❌ Error en el endpoint /consulta_factura: {str(e)}")
        return jsonify({"status": "error", "message": "Error interno del servidor"}), 500
    



#-----------------------------------------------------------------------------------------

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

@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

if __name__ == '__main__':
    app.run(debug=True)
