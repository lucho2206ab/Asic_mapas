-- BASE DE DATOS: gis_database (Ejemplo)
-- Crear la base de datos si no existe
-- CREATE DATABASE IF NOT EXISTS gis_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE gis_database;

-- Tabla para almacenar los datos GeoJSON de las capas
-- Usamos LONGTEXT para asegurarnos de que el JSON del GeoJSON (que puede ser grande) quepa.
CREATE TABLE IF NOT EXISTS geojson_layers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- Nombre único para identificar la capa (ej: 'red_riego', 'parcelario', 'parcelario_1104')
    layer_name VARCHAR(255) UNIQUE NOT NULL, 
    -- Descripción para referencia
    description VARCHAR(500), 
    -- El contenido completo del archivo GeoJSON
    geojson_data LONGTEXT NOT NULL, 
    -- Fecha de la última actualización
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ejemplo de inserción para la capa 'parcelario_1104' que proporcionaste.
-- NOTA: Debes reemplazar 'CONTENIDO_JSON_DE_PARCELARIO' con el contenido real del archivo Parcelario_1104_1106_1010_1016.geojson.
-- Esto se hace típicamente con un script de carga, pero aquí se muestra la estructura.

INSERT INTO geojson_layers (layer_name, description, geojson_data) 
VALUES (
    'parcelario_1104', 
    'Parcelario 1104 1106 1010 1016', 
    'CONTENIDO_JSON_DE_PARCELARIO' 
);