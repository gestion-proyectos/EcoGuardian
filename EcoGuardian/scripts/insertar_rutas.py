import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="bdecoguardian",
    user="postgres",
    password="2915790sol",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Lista de rutas
rutas = [
    "Calle 77 Sur-carrera46-calle75sur-carrera45-calle68sur-carrera43c",
    "calle77sur - carrera47- calle74sur-carrera46- calle73sur- carrera46cc-calle73sur- carrera45a-carrera45- carrera43c",
    "Calle 76 Sur, Carrera 46- Calle 69 Sur / Calle 71 Sur, Carrera 45, Carrera 43A-Calle 66 Sur, Carrera 43C",
    "Calle 77 Sur-Carrera 46D-Carrera 47C-Calle 74 Sur-Carrera 46C-Calle 72 Sur-Carrera 45A-Calle 71 Sur-Calle 69 Sur-Calle 67 Sur-Carrera 43C",
    "Calle 77 Sur-Carrera 45A-Calle 75 Sur-Carrera 44A-Calle 72 Sur-Carrera 45A-Calle 69 Sur-Carrera 43C",
    "Calle 77 Sur-carrera47-calle76sur-carrera47b-carrera47a-calle76sur-carrera46d-calle75sur-calle74asur-carrera44-calle73sur-carrera45-carrera43c",
    "carrera46b-calle78sur-carrera46d-calle77sur-carrera47b-carrera47a-calle76sur-calle75sur-carrera46a-calle74sur-calle73sur-carrera45-carrera43c",
    "carrera46b-calle78sur-carrera46d-calle77sur-carrera47b-carrera47a-calle75sur-carrera46a-calle74sur-carrera45a-carrera45-carrera43c",
    "Calle 77 Sur-carrera45-calle75sur-carrera46d- calle74sur-calle73sur-carrera45a-carrera46cc-calle66sur",
    "Calle 77 Sur-carrera47-calle76sur-carrera46b-calle74sur-carrera45a-carrera45-calle69sur-carrera44-carrera43c",
    "Calle 77 Sur-carrera47-carrera46e-carrera46cc-calle70sur-carrera46-calle69sur-calle68sur-carrera46-calle67sur-carrera45-calle66sur",
    "Calle 77 Sur-carrera47-calle76sur-carrera46cc-calle74sur-carrera46b-calle73sur-carrera46-calle69sur-carrera46a-calle67sur-calle66sur",
    "carrera46b-calle78sur-carrera46d-calle77sur-carrera47b-carrera47a-calle76sur-carrera46d-calle75sur-carrera45-calle66sur",
    "Calle 77 Sur-carrera47-calle76sur-carrera46-calle75sur-carrera45-calle74asur-carrera44-carrera45-calle71sur-carrera46-calle70sur-carrera45-calle66sur",
    "Calle 77 Sur-carrera47b-carrera47c-calle75sur-carrera46d-calle73sur-carrera46e-calle71sur-carrera46b-calle70sur-carrera46-calle69ur-carrera46a-calle67sur-calle66sur"
]

# Insertar rutas
for i, ruta in enumerate(rutas, start=1):
    calles = [c.strip().replace("/", "") for c in ruta.split("-")]
    cur.execute("""
        INSERT INTO rutas (id_ruta, nombre_ruta, origen, destino, calles)
        VALUES (%s, %s, %s, %s, %s)
    """, (i, f"Ruta {i}", "Hospital Venancio Díaz", "Parque de los 4 Elementos", calles))

conn.commit()
cur.close()
conn.close()

print("✅ Inserción completada.")
