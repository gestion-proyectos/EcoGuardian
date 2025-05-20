import psycopg2
import json

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="bdecoguardian",
    user="postgres",
    password="2915790sol",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Ruta del archivo GeoJSON
geojson_path = "../static/rutas_json/Ecoguardian_sabaneta.json"

# Cargar el archivo
with open(geojson_path, "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Recorrer las rutas y actualizar
for feature in geojson["features"]:
    nombre = feature["properties"]["name"].replace("#", "").strip()  # <-- esta es la clave
    coords = feature["geometry"]["coordinates"]

    cur.execute("""
        UPDATE rutas
        SET coordenadas = %s
        WHERE nombre_ruta = %s
    """, (json.dumps(coords), nombre))

conn.commit()
cur.close()
conn.close()

print("✅ Coordenadas actualizadas correctamente.")
