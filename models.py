from cassandra.cluster import Cluster
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import uuid
from collections import defaultdict
from tabulate import tabulate
import json

# ——————————————————————————————————————————————————————————————————
# 1) Definición de modelos (uno por cada tabla de tu esquema)
# ——————————————————————————————————————————————————————————————————
@dataclass
class SubAlcaldia:
    idSubAlcaldia: uuid.UUID
    nombreAlcaldia: str

@dataclass
class Distrito:
    idDistrito: uuid.UUID
    numeroDistrito: int
    fk_idSubAlcaldia: uuid.UUID

@dataclass
class SubDistrito:
    idSubDistrito: uuid.UUID
    numeroSubDistrito: int
    fk_idDistrito: uuid.UUID

@dataclass
class Antena:
    idAntena: uuid.UUID
    nombreAntena: str
    latitud: float
    longitud: float

@dataclass
class Zona:
    idZona: uuid.UUID
    nombreZona: str
    fk_idSubDistrito: uuid.UUID
    fk_idAntena: uuid.UUID

@dataclass
class Infraestructura:
    idInfraEstructura: uuid.UUID
    tipoInfraestructura: str

@dataclass
class Tarifario:
    idTarifario: uuid.UUID
    nombre: str
    tipoTarifario: str
    m3_mes: float
    us_mes: float

@dataclass
class UnidadesEducativas:
    idUnidadesEducativas: uuid.UUID
    codigo: str
    nombre: str
    dependencia: str
    zona: str
    direccion: str
    fk_idDistritos: uuid.UUID
    fk_idInfraEstructura: uuid.UUID
    fk_idTarifario: uuid.UUID

@dataclass
class Medidor:
    idMedidor: uuid.UUID
    macMedidor: str
    tipoMedidor: str
    marca: str
    modelo: str
    tipoConectividad: str
    aplicacion: str

@dataclass
class Usuario:
    idUsuario: uuid.UUID
    nombre: str
    telefono: str
    correoElectronico: str

@dataclass
class LecturaMedidor:
    idLectura: uuid.UUID
    fecha: datetime
    estado: int
    consumo: float
    tipoTarifario: str
    latitud: float
    longitud: float
    fk_idMedidor: uuid.UUID
    fk_idDistrito: uuid.UUID
    fk_idAntena: uuid.UUID
    fk_idUsuario: uuid.UUID
    error: str

@dataclass
class InfraestructuraPublica:
    idInfraPublica: uuid.UUID
    nombreInfraPublica: str
    latitud: float
    longitud: float
    fk_idInfraestructura: uuid.UUID
    fk_idDistrito: uuid.UUID
    fk_idTarifario: uuid.UUID

@dataclass
class Contrato:
    idContrato: uuid.UUID
    numeroContrato: str
    fechaInicio: datetime
    fechaFin: datetime
    fk_idUsuario: uuid.UUID

@dataclass
class ContratoMedidor:
    idContratoMedidor: uuid.UUID
    esPrimero: bool
    descripcion: str
    fechaAsignacion: datetime
    fk_idContrato: uuid.UUID
    fk_idMedidor: uuid.UUID


# ——————————————————————————————————————————————————————————————————
# 2) Cargar todas las tablas en listas de objetos
# ——————————————————————————————————————————————————————————————————
def get_session(keyspace='semapa'):
    cluster = Cluster(['127.0.0.1'])
    return cluster.connect(keyspace)

def load_table(model_cls, table_name: str) -> List:
    sess = get_session()
    rows = sess.execute(f"SELECT * FROM {table_name} ALLOW FILTERING")
    objs = []
    for row in rows:
        data = row._asdict()  # p.ej. {'idsubalcaldia': UUID(...), 'nombrealcaldia': 'TUNARI'}
        # Construimos el dict de init solo con las keys que model_cls espera
        init_kwargs = {}
        for field in model_cls.__annotations__:
            key = field.lower()  # 'idSubAlcaldia' -> 'idsubalcaldia'
            if key in data:
                init_kwargs[field] = data[key]
        objs.append(model_cls(**init_kwargs))
    return objs


# Carga todo
subalcaldias         = load_table(SubAlcaldia,         'SubAlcaldia')
distritos            = load_table(Distrito,            'Distrito')
subdistritos         = load_table(SubDistrito,         'SubDistrito')
antenas              = load_table(Antena,              'Antena')
zonas                = load_table(Zona,                'Zona')
infraestructuras     = load_table(Infraestructura,     'Infraestructura')
tarifarios           = load_table(Tarifario,           'Tarifario')
unidades_educativas  = load_table(UnidadesEducativas,  'UnidadesEducativas')
medidores            = load_table(Medidor,            'Medidor')
usuarios             = load_table(Usuario,             'Usuario')
lecturas             = load_table(LecturaMedidor,      'LecturaMedidor')
infra_pub            = load_table(InfraestructuraPublica,'InfraestructuraPublica')
contratos            = load_table(Contrato,            'Contrato')
contrato_medidor     = load_table(ContratoMedidor,     'ContratoMedidor')
