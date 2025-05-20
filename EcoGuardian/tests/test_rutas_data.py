import json
import os
import pytest

def load_rutas_json():
    """Carga el archivo JSON de rutas"""
    json_path = os.path.join('static', 'rutas_json', 'Ecoguardian_sabaneta.json')
    with open(json_path, 'r') as f:
        return json.load(f)

def test_estructura_geojson():
    """Prueba la estructura básica del GeoJSON"""
    data = load_rutas_json()
    
    # Verificar estructura general
    assert 'type' in data
    assert data['type'] == 'FeatureCollection'
    assert 'features' in data
    assert isinstance(data['features'], list)
    assert len(data['features']) > 0

def test_estructura_rutas():
    """Prueba la estructura de cada ruta"""
    data = load_rutas_json()
    
    for feature in data['features']:
        # Verificar estructura de feature
        assert 'type' in feature
        assert feature['type'] == 'Feature'
        assert 'geometry' in feature
        assert 'properties' in feature
        
        # Verificar geometría
        geometry = feature['geometry']
        assert geometry['type'] == 'LineString'
        assert 'coordinates' in geometry
        assert isinstance(geometry['coordinates'], list)
        assert len(geometry['coordinates']) >= 2
        
        # Verificar propiedades
        properties = feature['properties']
        assert 'name' in properties
        assert 'criticidad' in properties
        assert properties['criticidad'] in ['baja', 'media', 'alta']

def test_coordenadas_validas():
    """Prueba que las coordenadas están dentro de rangos válidos"""
    data = load_rutas_json()
    
    for feature in data['features']:
        for coord in feature['geometry']['coordinates']:
            # Verificar longitud (debe estar entre -180 y 180)
            assert -180 <= coord[0] <= 180
            # Verificar latitud (debe estar entre -90 y 90)
            assert -90 <= coord[1] <= 90

def test_coordenadas_sabaneta():
    """Prueba que las coordenadas están dentro del área de Sabaneta"""
    data = load_rutas_json()
    
    # Coordenadas aproximadas de Sabaneta
    sabaneta_bounds = {
        'lon_min': -75.65,
        'lon_max': -75.60,
        'lat_min': 6.14,
        'lat_max': 6.16
    }
    
    for feature in data['features']:
        for coord in feature['geometry']['coordinates']:
            lon, lat = coord
            assert sabaneta_bounds['lon_min'] <= lon <= sabaneta_bounds['lon_max']
            assert sabaneta_bounds['lat_min'] <= lat <= sabaneta_bounds['lat_max']

def test_nombres_rutas():
    """Prueba que los nombres de las rutas son únicos"""
    data = load_rutas_json()
    nombres = [feature['properties']['name'] for feature in data['features']]
    assert len(nombres) == len(set(nombres))

def test_criticidad_valida():
    """Prueba que todas las rutas tienen una criticidad válida"""
    data = load_rutas_json()
    criticidades_validas = ['baja', 'media', 'alta']
    
    for feature in data['features']:
        criticidad = feature['properties']['criticidad']
        assert criticidad in criticidades_validas

def test_continuidad_rutas():
    """Prueba que las rutas son continuas (no hay saltos grandes entre puntos)"""
    data = load_rutas_json()
    
    for feature in data['features']:
        coords = feature['geometry']['coordinates']
        for i in range(len(coords) - 1):
            # Calcular distancia entre puntos consecutivos
            lon1, lat1 = coords[i]
            lon2, lat2 = coords[i + 1]
            
            # La distancia no debe ser mayor a 0.01 grados (aproximadamente 1km)
            assert abs(lon2 - lon1) < 0.01
            assert abs(lat2 - lat1) < 0.01 