from flask import Flask, render_template, Response
import json
import os
from pathlib import Path
import mysql.connector 

app = Flask(__name__)

# =============================================================
# CONFIGURACIÓN DE CONEXIÓN A LA BASE DE DATOS (BD)
# =============================================================
# NOTA: Debes reemplazar estos valores con tus credenciales reales de MySQL.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'gis_database' 
}

# La ruta donde están tus archivos GeoJSON de fallback
STATIC_DATA_DIR = Path(app.static_folder) / 'data'
if app.static_folder is None:
    # Esto es solo un fallback de desarrollo, normalmente Flask lo define
    STATIC_DATA_DIR = Path('static') / 'data'

# =============================================================
# FUNCIÓN CENTRAL DE EXTRACCIÓN DE DATOS (CON SIMULACIÓN DE BD)
# =============================================================
def get_geojson_from_source(layer_name):
    """
    Simula la obtención de datos GeoJSON, priorizando la BD y cayendo a archivos locales.
    
    layer_name: Nombre de la capa (ej: 'red_riego', 'parcelario_derecho_superior', etc.)
    """
    
    # 1. INTENTAR CONEXIÓN Y CONSULTA A MYSQL (Lógica comentada para tu implementación)
    
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        # Consultar el GeoJSON por el nombre de la capa
        query = ("SELECT geojson_data FROM geojson_layers WHERE layer_name = %s")
        cursor.execute(query, (layer_name,))
        
        result = cursor.fetchone()
        
        if result:
            print(f"DEBUG: Capa '{layer_name}' obtenida de la BD.")
            # La base de datos almacena el texto, lo devolvemos como JSON
            return json.loads(result[0]) 
            
    except mysql.connector.Error as err:
        print(f"ERROR: No se pudo conectar a MySQL o ejecutar la consulta: {err}")
        # Continuar al fallback si hay un error de BD
    finally:
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()
    
    
    # 2. FALLBACK: Leer GeoJSON desde archivo local (hasta que la BD esté lista)
    
    # Mapeo de nombres de API a nombres de archivo:
    # Debes usar el nombre de archivo sin la extensión, o definir un mapeo explícito.
    # Por simplicidad, usaremos un mapeo explícito para evitar errores de nombres.
    
    layer_to_filename = {
        'red_riego': 'RedRiegoPrimeraZona_wgs84.geojson',
        'parcelario_derecho_superior': 'ParcelarioRioMendoza-DerechoSuperior_wgs84.geojson',
        'asociaciones': 'asociaciones.json',
        'cuencas': 'cuencas.json',
        'red_primaria': 'red-primaria.json',
        'derechos_superficiales': 'DerechosSuperficialesRioMendoza.geojson',
        'parcelario_1104': 'Parcelario_1104_1106_1010_1016.geojson',
        '1010-2025_convertido_wgs84': '1010-2025_convertido_wgs84.geojson',
        'der_superficiales_nuevo': 'DerSuperfNuevo_wgs84.geojson',
        # Añade más capas aquí...
    }
    
    filename = layer_to_filename.get(layer_name)
    
    if filename:
        filepath = STATIC_DATA_DIR / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"DEBUG: Capa '{layer_name}' cargada desde archivo local: {filepath}")
                return data
        except FileNotFoundError:
            print(f"ERROR: Archivo no encontrado en el fallback: {filepath}")
        except json.JSONDecodeError:
            print(f"ERROR: Error al decodificar JSON del archivo: {filepath}")

    # Devolver una GeoJSON FeatureCollection vacía si falla todo
    return {"type": "FeatureCollection", "features": []}

# =============================================================


# 1. RUTA PRINCIPAL: Sirve tu HTML
@app.route('/')
def serve_map_page():
    # Flask buscará 'prueba.html' dentro de la carpeta 'templates/'
    return render_template('prueba.html') 

# 2. RUTA API: Sirve el GeoJSON solicitado
@app.route('/api/geojson/<layer_name>', methods=['GET'])
def get_layer_geojson(layer_name):
    
    # Obtener los datos GeoJSON
    geojson_data = get_geojson_from_source(layer_name)
    
    # Devuelve los datos como GeoJSON (application/json)
    return Response(
        json.dumps(geojson_data),
        mimetype='application/json'
    )

if __name__ == '__main__':
    # Asegúrate de crear la carpeta 'static/data' y colocar tus GeoJSON/JSON dentro
    if not STATIC_DATA_DIR.exists():
        os.makedirs(STATIC_DATA_DIR)
        print(f"ADVERTENCIA: Se ha creado el directorio de datos de fallback: {STATIC_DATA_DIR}")

    print("Iniciando Flask. Asegúrate de que tus archivos GeoJSON estén en static/data/")
    app.run(debug=True)
