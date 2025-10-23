import json
import os
from pathlib import Path
import mysql.connector
from mysql.connector import errorcode

# =============================================================
# CONFIGURACIÓN DE CONEXIÓN A LA BASE DE DATOS (AJUSTAR ESTO)
# =============================================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'root', 
    'database': 'gis_database' 
}

# La carpeta donde tienes tus archivos GeoJSON/JSON
# Asume que este script está en el mismo directorio que tu app.py
DATA_DIR = Path('./static/data') 

# Mapeo de nombres de API (usados en app.py) a nombres de archivo
# Asegúrate de que esta lista cubra TODAS tus capas:
LAYER_MAPPING = {
    'red_riego': 'RedRiegoPrimeraZona_wgs84.geojson',
    'parcelario_derecho_superior': 'ParcelarioRioMendoza-DerechoSuperior_wgs84.geojson',
    'asociaciones': 'asociaciones.json',
    'cuencas': 'cuencas.json',
    'red_primaria': 'red-primaria.json',
    'derechos_superficiales': 'DerechosSuperficialesRioMendoza.geojson',
    'parcelario_1104': 'Parcelario_1104_1106_1010_1016.geojson'
}

def load_geojson_to_mysql():
    """
    Lee archivos GeoJSON de la carpeta local y los inserta/actualiza en MySQL.
    """
    cnx = None
    try:
        # Conectar a la base de datos
        print("Conectando a la base de datos...")
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        print("Conexión exitosa.")

        # Consulta SQL para insertar o actualizar (si el layer_name ya existe)
        add_layer = ("INSERT INTO geojson_layers "
                     "(layer_name, description, geojson_data) "
                     "VALUES (%s, %s, %s) "
                     "ON DUPLICATE KEY UPDATE geojson_data = VALUES(geojson_data), description = VALUES(description)")

        for layer_name, filename in LAYER_MAPPING.items():
            filepath = DATA_DIR / filename
            description = f"Datos de la capa {layer_name} (Origen: {filename})"
            
            if not filepath.exists():
                print(f"ADVERTENCIA: Archivo no encontrado para la capa '{layer_name}': {filepath}")
                continue
                
            print(f"Procesando capa: {layer_name}...")

            try:
                # Leer el contenido completo del archivo GeoJSON
                with open(filepath, 'r', encoding='utf-8') as f:
                    # Leemos el JSON y lo volcamos a string para guardarlo en LONGTEXT
                    geojson_data = json.dumps(json.load(f))
                    
                # Preparar los datos para la inserción
                data_layer = (layer_name, description, geojson_data)

                # Ejecutar la consulta
                cursor.execute(add_layer, data_layer)
                print(f"  -> Capa '{layer_name}' cargada/actualizada correctamente.")

            except FileNotFoundError:
                print(f"ERROR: No se encontró el archivo: {filepath}")
            except json.JSONDecodeError:
                print(f"ERROR: El archivo no es un JSON válido: {filepath}")
            except Exception as e:
                print(f"ERROR al procesar '{layer_name}': {e}")
                
        # Confirmar todos los cambios
        cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERROR: Credenciales de MySQL incorrectas.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"ERROR: La base de datos '{DB_CONFIG['database']}' no existe.")
        else:
            print(f"ERROR de conexión a MySQL: {err}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        if cnx and cnx.is_connected():
            cursor.close()
            cnx.close()
            print("Proceso de carga finalizado. Conexión a MySQL cerrada.")

if __name__ == '__main__':
    # Ejecuta este script para cargar tus datos
    load_geojson_to_mysql()
