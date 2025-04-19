# 🌿 EcoGuardian

**EcoGuardian** es una aplicación web que permite a los ciudadanos consultar rutas optimizadas entre dos puntos fijos, evitando zonas afectadas por eventos ambientales nocivos para la salud, como contaminación, incendios. Estas alertas son generadas en tiempo real a partir de reportes ciudadanos.

---

## 🧾 Descripción del Proyecto

El propósito principal de EcoGuardian es proporcionar una herramienta útil, educativa y accionable para las personas que quieren conocer el estado del aire en su entorno, proteger su salud y tomar decisiones informadas.  

A través de una plataforma sencilla y accesible, el sistema muestra mapas, permite reportar eventos ambientales, y entrega notificaciones personalizadas.

---

## 📁 Estructura del Proyecto

```plaintext
EcoGuardian/
├── app/                            # Lógica principal de la aplicación
│   ├── __init__.py                 # Inicializa la app y carga configuraciones
│   ├── routes.py                   # Definición de rutas y controladores
│   ├── models.py                   # Modelos de base de datos (SQLAlchemy)
│   ├── services/                   # Lógica modular (ej. notificaciones, reportes)
│   │   └── air_quality.py
│   └── templates/                  # Plantillas HTML (Jinja2)
│       └── index.html
├── static/                         # Archivos estáticos: CSS, JS, imágenes
│   ├── css/
│   └── js/
├── config.py                       # Configuración global del proyecto
├── .env                            # Variables de entorno (API keys, DB, etc.)
├── requirements.txt               # Dependencias del proyecto
├── run.py                          # Punto de entrada para ejecutar la app
└── README.md                       # Documentación del proyecto
```````

---

## ⚙️ Funcionalidades

- 🗺️ Mapa interactivo de calidad del aire
- 📢 Notificaciones y alertas en tiempo real
- 🔥 Reportes ciudadanos de eventos ambientales
- 🩺 Recomendaciones de salud personalizadas
- 🧾 Historial de calidad del aire
- 👤 Registro e inicio de sesión con configuración de perfil

---

## 📌 Consideraciones

- El desarrollo del proyecto se organiza usando **GitHub Projects**.
- El enfoque está limitado a una **zona geográfica específica** para mejorar la precisión del análisis.
- El proyecto está en etapa de desarrollo activo; algunos módulos aún están en construcción.
- Se utiliza **Flask** como framework backend y **PostgreSQL** como sistema de base de datos.
- Puedes contribuir siguiendo la estructura del proyecto, generando ramas y enviando pull requests.

---
## 🎯 Objetivo del Proyecto

Desarrollar un modelo de optimización de rutas entre dos puntos fijos georreferenciados, utilizando datos ambientales reportados por los usuarios en el territorio. El objetivo es evitar zonas con eventos nocivos para la salud y así ofrecer alternativas más seguras para la movilidad ciudadana.

---

## 🌐 Prototipo

Puedes visualizar un prototipo inicial en Figma:  
🔗 [Prototipo EcoGuardian](https://www.figma.com/proto/3gqMd3edEjIf25vP4GZGiY/EcoGuardian?node-id=22-8&t=bIS0fmMzYwTap3u7-1&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=22%3A8)

---

## 📄 Licencia

Este proyecto es de código abierto bajo la licencia [MIT](https://opensource.org/licenses/MIT).
