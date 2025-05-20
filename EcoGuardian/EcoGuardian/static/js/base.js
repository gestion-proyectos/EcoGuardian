// Función para inicializar el mapa
function initializeMap() {
  map = L.map('map', {
    center: [6.2447, -75.5748],
    zoom: 13,
    zoomControl: false
  });

  L.control.zoom({
    position: 'bottomright'
  }).addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
}

// Llamar a la función cuando el documento esté listo
document.addEventListener('DOMContentLoaded', initializeMap);

function moveFrame(event, section) {
  const frame31 = document.getElementById('frame31');
  const buttons = document.querySelectorAll('.menu-button');

  // Remueve clase activa
  buttons.forEach(btn => btn.classList.remove('active'));

  // Agrega clase activa al clicado
  event.target.classList.add('active');

  // Contenido dinámico
  switch (section) {
    case 'datos':
      frame31.innerHTML = 'Datos personales';
      break;
    case 'condiciones':
      frame31.innerHTML = 'Condiciones de salud';
      break;
    case 'estilo':
      frame31.innerHTML = 'Estilo de vida activo';
      break;
  }
}

// Verificar si hay una sesión activa
function isLoggedIn() {
  return "{{ session.get('username') }}" !== "";
}

// Función para verificar la sesión antes de mostrar el menú
function checkSession(type) {
  if (!isLoggedIn()) {
    // Redirigir al login si no hay sesión
    window.location.href = "{{ url_for('idvistalogin.vista_login') }}";
    return;
  }
  showMiniMenu(type);
}

function showMiniMenu(type) {
  const menu = document.getElementById('miniMenu');
  const content = document.getElementById('miniMenuContent');
  content.innerHTML = '';

  // Limpia el contenido anterior
  menu.classList.remove('menu-ecoeventos', 'menu-rutas', 'menu-reportes', 'menu-usuarios');

  let items = [];

  if (type === 'eventos') {
    items = [
      { label: 'Ver puntos de incendio', link: '/ver_incendios' },
      { label: 'ver zonas con alta contaminación', link: '/ver_contaminacion' },
      { label: 'ver zonas con polen', link: '/ver_polen' }
    ];
    menu.classList.add('menu-ecoeventos');


  } else if (type === 'rutas') {
    items = [
      { label: 'Inciar', link: '/ver_rutas_guardadas' },
      /*         { label: 'Iniciar ruta guardada', link: '/iniciar_ruta' },
              { label: 'Añadir ruta', link: '/añadir_ruta' } */
    ];
    menu.classList.add('menu-rutas');


  } else if (type === 'reportes') {
    items = [
      { label: 'Incendios', link: '/reportar_incendio' },
      { label: 'Contaminación alta', link: '/reportar_contaminacion' },
      { label: 'polen', link: '/reportar_polen' }
    ];
    menu.classList.add('menu-reportes');


  } else if (type === 'usuarios') {
    items = [
      { label: 'iniciarsesion(breve)', link: '/login' },
      { label: 'Editar perfil', link: "{{ url_for('idvistaeditarperfil.vista_editar_perfil') }}" },
      { label: 'Cerrar sesión', link: "{{ url_for('home.logout') }}" }
    ];
    menu.classList.add('menu-usuarios');
  }

  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.label;
    li.onclick = () => {
      window.location.href = item.link;
    };
    content.appendChild(li);
  });

  menu.classList.remove('hidden');
}

// Ocultar el mini menú si haces clic fuera
document.addEventListener('click', function (e) {
  const menu = document.getElementById('miniMenu');
  if (!menu.contains(e.target) && !e.target.classList.contains('trigger-btn')) {
    menu.classList.add('hidden');
  }
});

// Función para geocodificar la dirección
async function geocodificarDireccion(direccion) {
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(direccion)}&format=json&limit=1`, {
      headers: {
        'User-Agent': 'EcoGuardian/1.0',
        'Accept': 'application/json'
      }
    });
    const data = await response.json();
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat);
      const lon = parseFloat(data[0].lon);
      return { lat, lon };
    }
    return null;
  } catch (error) {
    console.error('Error en geocodificación:', error);
    return null;
  }
}

let map;  // variable global
// Variable para mantener el marcador actual
let currentMarker = null;

// Escuchar cambios en el campo de dirección
document.getElementById('calle_afectada').addEventListener('change', async function () {
  const direccion = this.value;
  if (direccion) {
    const coords = await geocodificarDireccion(direccion);
    if (coords) {
      // Eliminar marcador anterior si existe
      if (currentMarker) {
        map.removeLayer(currentMarker);
      }
      // Crear nuevo marcador
      currentMarker = L.marker([coords.lat, coords.lon]).addTo(map);
      // Centrar el mapa en la nueva ubicación
      map.setView([coords.lat, coords.lon], 15);
    }
  }
});