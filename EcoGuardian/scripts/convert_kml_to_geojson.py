import xml.etree.ElementTree as ET
import json

# Rutas corregidas (solo un nivel arriba desde scripts/)
kml_path = "../document/Ecoguardian_sabaneta.kml"
geojson_path = "../static/rutas_json/Ecoguardian_sabaneta.json"

# Parsear el KML
tree = ET.parse(kml_path)
root = tree.getroot()
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

features = []
for placemark in root.findall('.//kml:Placemark', namespace):
    name = placemark.find('kml:name', namespace).text if placemark.find('kml:name', namespace) is not None else 'Sin nombre'
    line = placemark.find('.//kml:LineString', namespace)
    if line is not None:
        coords_text = line.find('kml:coordinates', namespace).text.strip()
        coords = [[float(c.split(',')[0]), float(c.split(',')[1])] for c in coords_text.split()]
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {"name": name, "criticidad": "media"}
        })

geojson = {"type": "FeatureCollection", "features": features}
with open(geojson_path, 'w', encoding='utf-8') as f:
    json.dump(geojson, f, indent=2)

print("✅ Conversión completada")
print("📁 Archivo guardado en:", geojson_path)
