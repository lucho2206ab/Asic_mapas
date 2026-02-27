# API de Capas Geoespaciales - Mi Riego

Este proyecto es una pequeña API desarrollada con Flask que permite servir capas geoespaciales en formato **GeoJSON** para ser consumidas por la aplicación **Mi Riego**.

Las capas son almacenadas en la carpeta `static/data` y se sirven automáticamente mediante endpoints HTTP.

El objetivo es facilitar la visualización de información geográfica en el frontend de la aplicación (parcelas, sectores, etc.).

---

## Tecnologías utilizadas

- Python
- Flask
- GeoPandas
- GeoJSON

---

## Estructura del proyecto

project/
│
├── app.py
├── convertsor_capas.py
├── requirements.txt
├── README.md
│
└── static/
└── data/
1010-2025_convertido_wgs84.geojson
DerSuperfNuevo_wgs84.geojson

---

## Sistema de coordenadas

Todas las capas deben estar en:
WGS84 (EPSG:4326)
Este sistema es el estándar utilizado por la mayoría de aplicaciones web de mapas.
Si una capa está en otro sistema de coordenadas puede convertirse usando el script:
convertsor_capas.py

---

## Instalación

1 Clonar el repositorio

git clone https://github.com/usuario/mi-riego-api.git
cd mi-riego-api

2 Crear entorno virtual

python -m venv venv

Activar entorno:
Linux / Mac >>>  source venv/bin/activate
Windows >>>  venv\Scripts\activate

3 Instalar dependencias

pip install -r requirements.txt

El servidor se iniciará en: http://localhost:5000

---

## Endpoints disponibles

### Listar capas disponibles

GET /layers

Devuelve la lista de archivos GeoJSON disponibles en `static/data`.

Ejemplo de respuesta:

[
"1010-2025_convertido_wgs84.geojson",
"DerSuperfNuevo_wgs84.geojson"
]

---

### Obtener una capa

GET /layer/<nombre_archivo>

Ejemplo:

http://localhost:5000/layer/1010-2025_convertido_wgs84.geojson

Devuelve la capa en formato **GeoJSON**.

---

## Conversión de capas

El script `convertsor_capas.py` permite convertir capas geoespaciales a **WGS84 (EPSG:4326)**.

Ejemplo:

python convertsor_capas.py archivo_original.shp

El script generará un nuevo archivo listo para ser utilizado por la API.

---

## Uso en la aplicación Mi Riego

La API está diseñada para ser consumida por la aplicación **Mi Riego**, permitiendo:

- visualizar parcelas
- mostrar sectores de riego
- integrar información geográfica en mapas interactivos
- servir capas GeoJSON de forma simple

---

## Autor

Proyecto desarrollado como soporte geoespacial para la aplicación **Mi Riego**.

