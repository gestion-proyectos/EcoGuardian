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
  return "{{ session.get('username') | default('') }}" !== "";
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
      { label: 'Ver zonas con alta contaminación', link: '/ver_contaminacion' },
      { label: 'Ver zonas con polen', link: '/ver_polen' }
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
      { label: 'Polen', link: '/reportar_polen' }
    ];
    menu.classList.add('menu-reportes');


  } else if (type === 'usuarios') {
    items = [
      { label: 'Iniciar sesión', link: '/login' },
      { label: 'Editar perfil', link: '/editar_perfil' },
      { label: 'Cerrar sesión', link: '/logout' }
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
const inputCalle = document.getElementById('calle_afectada');
if (inputCalle) {
  inputCalle.addEventListener('change', async function () {
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
}

if (window.REPORTES_INCENDIOS) {
  // Inicializar el mapa solo si hay reportes de incendios
  const map = L.map('map', {
    center: [-17.7833, -63.1821],
    zoom: 13,
    zoomControl: false // Desactiva el control de zoom por defecto
  });

  // Agrega el control de zoom en la parte inferior derecha
  L.control.zoom({
    position: 'bottomright'
  }).addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  const fireIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const bounds = [];
  window.REPORTES_INCENDIOS.forEach(function (reporte) {
    if (reporte.lat && reporte.lon) {
      const coords = [parseFloat(reporte.lat), parseFloat(reporte.lon)];
      const marker = L.marker(coords, { icon: fireIcon }).addTo(map);
      bounds.push(coords);

      const contenido = `
        <div style="font-family: Arial, sans-serif; padding: 10px;">
          <h6 style="margin: 0 0 10px 0; color: #d9534f;">Reporte de Incendio</h6>
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Severidad:</th>
              <td style="padding: 5px;">${reporte.severidad}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Descripción:</th>
              <td style="padding: 5px;">${reporte.descripcion}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Fecha:</th>
              <td style="padding: 5px;">${reporte.fecha_reporte}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Calle:</th>
              <td style="padding: 5px;">${reporte.calle_afectada}</td>
            </tr>
          </table>
          <div style="margin-top:10px;">
            <button class="btn-like" data-id="${reporte.id_reporte}">👍</button>
            <button class="btn-dislike" data-id="${reporte.id_reporte}">👎</button>
          </div>
          <div style="margin-top:10px;">
            <textarea class="comentario" data-id="${reporte.id_reporte}" placeholder="Agrega un comentario"></textarea>
            <button class="btn-comentar" data-id="${reporte.id_reporte}">Comentar</button>
          </div>
          <div style="margin-top:10px;">
            <button class="btn-ver-comentarios" data-id="${reporte.id_reporte}">Ver comentarios</button>
            <div class="comentarios-lista" data-id="${reporte.id_reporte}" style="display: none; margin-top: 10px; max-height: 200px; overflow-y: auto;">
              <div class="comentarios-contenido"></div>
            </div>
          </div>
        </div>
      `;
      marker.bindPopup(contenido);
    }
  });

  if (bounds.length > 0) {
    map.fitBounds(bounds);
  }
}

if (window.REPORTES_CONTAMINACION) {
  // Inicializar el mapa solo si hay reportes de contaminación
  const map = L.map('map', {
    center: [-17.7833, -63.1821], // Cambia el centro si lo necesitas
    zoom: 13,
    zoomControl: false // Desactiva el control de zoom por defecto
  });

  // Agrega el control de zoom en la parte inferior derecha
  L.control.zoom({
    position: 'bottomright'
  }).addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Puedes usar un icono diferente para contaminación si lo deseas
  const pollutionIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const bounds = [];
  window.REPORTES_CONTAMINACION.forEach(function (reporte) {
    if (reporte.lat && reporte.lon) {
      const coords = [parseFloat(reporte.lat), parseFloat(reporte.lon)];
      const marker = L.marker(coords, { icon: pollutionIcon }).addTo(map);
      bounds.push(coords);

      const contenido = `
        <div style="font-family: Arial, sans-serif; padding: 10px;">
          <h6 style="margin: 0 0 10px 0; color: #28a745;">Reporte de Contaminación</h6>
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Severidad:</th>
              <td style="padding: 5px;">${reporte.severidad}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Descripción:</th>
              <td style="padding: 5px;">${reporte.descripcion}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Fecha:</th>
              <td style="padding: 5px;">${reporte.fecha_reporte}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Calle:</th>
              <td style="padding: 5px;">${reporte.calle_afectada}</td>
            </tr>
          </table>
          <div style="margin-top:10px;">
            <button class="btn-like" data-id="${reporte.id_reporte}">👍</button>
            <button class="btn-dislike" data-id="${reporte.id_reporte}">👎</button>
          </div>
          <div style="margin-top:10px;">
            <textarea class="comentario" data-id="${reporte.id_reporte}" placeholder="Agrega un comentario"></textarea>
            <button class="btn-comentar" data-id="${reporte.id_reporte}">Comentar</button>
          </div>
          <div style="margin-top:10px;">
            <button class="btn-ver-comentarios" data-id="${reporte.id_reporte}">Ver comentarios</button>
            <div class="comentarios-lista" data-id="${reporte.id_reporte}" style="display: none; margin-top: 10px; max-height: 200px; overflow-y: auto;">
              <div class="comentarios-contenido"></div>
            </div>
          </div>
        </div>
      `;
      marker.bindPopup(contenido);
    }
  });

  if (bounds.length > 0) {
    map.fitBounds(bounds);
  }
}

if (window.REPORTES_POLEN) {
  // Inicializar el mapa solo si hay reportes de polen
  const map = L.map('map', {
    center: [-17.7833, -63.1821], // Cambia el centro si lo necesitas
    zoom: 13,
    zoomControl: false // Desactiva el control de zoom por defecto
  });

  // Agrega el control de zoom en la parte inferior derecha
  L.control.zoom({
    position: 'bottomright'
  }).addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Icono personalizado para polen (puedes cambiar el color si lo deseas)
  const pollenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const bounds = [];
  window.REPORTES_POLEN.forEach(function (reporte) {
    if (reporte.lat && reporte.lon) {
      const coords = [parseFloat(reporte.lat), parseFloat(reporte.lon)];
      const marker = L.marker(coords, { icon: pollenIcon }).addTo(map);
      bounds.push(coords);

      const contenido = `
        <div style="font-family: Arial, sans-serif; padding: 10px;">
          <h6 style="margin: 0 0 10px 0; color: #ffc107;">Reporte de Polen</h6>
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Severidad:</th>
              <td style="padding: 5px;">${reporte.severidad}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Descripción:</th>
              <td style="padding: 5px;">${reporte.descripcion}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Fecha:</th>
              <td style="padding: 5px;">${reporte.fecha_reporte}</td>
            </tr>
            <tr>
              <th style="text-align: left; padding: 5px; background: #f8f9fa;">Calle:</th>
              <td style="padding: 5px;">${reporte.calle_afectada}</td>
            </tr>
          </table>
          <div style="margin-top:10px;">
            <button class="btn-like" data-id="${reporte.id_reporte}">👍</button>
            <button class="btn-dislike" data-id="${reporte.id_reporte}">👎</button>
          </div>
          <div style="margin-top:10px;">
            <textarea class="comentario" data-id="${reporte.id_reporte}" placeholder="Agrega un comentario"></textarea>
            <button class="btn-comentar" data-id="${reporte.id_reporte}">Comentar</button>
          </div>
          <div style="margin-top:10px;">
            <button class="btn-ver-comentarios" data-id="${reporte.id_reporte}">Ver comentarios</button>
            <div class="comentarios-lista" data-id="${reporte.id_reporte}" style="display: none; margin-top: 10px; max-height: 200px; overflow-y: auto;">
              <div class="comentarios-contenido"></div>
            </div>
          </div>
        </div>
      `;
      marker.bindPopup(contenido);
    }
  });

  if (bounds.length > 0) {
    map.fitBounds(bounds);
  }
}

// Función para enviar la reacción al backend
async function enviarReaccion(idReporte, tipoReaccion, comentario) {
  try {
    const response = await fetch('/api/reaccion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id_reporte: idReporte,
        tipo_reaccion: tipoReaccion,
        comentario: comentario
      }),
      credentials: 'same-origin'
    });

    const data = await response.json();
    
    if (!response.ok) {
      if (response.status === 401) {
        alert('Por favor, inicia sesión para poder reaccionar o comentar.');
        window.location.href = data.redirect || '/login';
        return;
      }
      throw new Error(data.message || 'Error al enviar la reacción');
    }

    return data;
  } catch (error) {
    console.error('Error:', error);
    if (error.message.includes('no autenticado')) {
      alert('Por favor, inicia sesión para poder reaccionar o comentar.');
      window.location.href = '/login';
    } else {
      alert(error.message || 'Error al procesar la acción');
    }
    throw error;
  }
}

// Delegación de eventos para los popups de Leaflet
document.addEventListener('click', async function (e) {
  try {
    // LIKE
    if (e.target.classList.contains('btn-like')) {
      const idReporte = e.target.getAttribute('data-id');
      const result = await enviarReaccion(idReporte, 'positivo', '');
      if (result && result.status === 'ok') {
        e.target.classList.add('active');
        const dislikeBtn = e.target.parentElement.querySelector('.btn-dislike');
        if (dislikeBtn) dislikeBtn.classList.remove('active');
        alert('¡Gracias por tu like!');
      }
    }
    // DISLIKE
    else if (e.target.classList.contains('btn-dislike')) {
      const idReporte = e.target.getAttribute('data-id');
      const result = await enviarReaccion(idReporte, 'negativo', '');
      if (result && result.status === 'ok') {
        e.target.classList.add('active');
        const likeBtn = e.target.parentElement.querySelector('.btn-like');
        if (likeBtn) likeBtn.classList.remove('active');
        alert('¡Gracias por tu feedback!');
      }
    }
    // COMENTARIO
    else if (e.target.classList.contains('btn-comentar')) {
      const idReporte = e.target.getAttribute('data-id');
      const textarea = document.querySelector(`textarea.comentario[data-id="${idReporte}"]`);
      const comentario = textarea.value.trim();
      
      if (comentario === '') {
        alert('Por favor, escribe un comentario.');
        return;
      }
      
      const result = await enviarReaccion(idReporte, 'neutral', comentario);
      if (result && result.status === 'ok') {
        textarea.value = '';
        
        // Mostrar el comentario en la interfaz
        const comentariosContainer = textarea.parentElement.querySelector('.comentarios-lista') || 
          document.createElement('div');
        comentariosContainer.classList.add('comentarios-lista');
        
        const comentarioElement = document.createElement('div');
        comentarioElement.classList.add('comentario-item');
        comentarioElement.textContent = comentario;
        comentariosContainer.appendChild(comentarioElement);
        
        if (!textarea.parentElement.querySelector('.comentarios-lista')) {
          textarea.parentElement.appendChild(comentariosContainer);
        }
        
        alert('¡Comentario enviado!');
      }
    }
    // VER COMENTARIOS
    else if (e.target.classList.contains('btn-ver-comentarios')) {
      const idReporte = e.target.getAttribute('data-id');
      const comentariosLista = document.querySelector(`.comentarios-lista[data-id="${idReporte}"]`);
      const comentariosContenido = comentariosLista.querySelector('.comentarios-contenido');
      
      try {
        const response = await fetch(`/api/comentarios/${idReporte}`);
        const data = await response.json();
        
        if (data.status === 'ok') {
          comentariosContenido.innerHTML = '';
          if (data.comentarios && data.comentarios.length > 0) {
            data.comentarios.forEach(comentario => {
              const comentarioElement = document.createElement('div');
              comentarioElement.style.padding = '5px';
              comentarioElement.style.borderBottom = '1px solid #eee';
              comentarioElement.innerHTML = `
                <div style="font-weight: bold;">${comentario.usuario}</div>
                <div>${comentario.comentario}</div>
                <div style="font-size: 0.8em; color: #666;">${comentario.fecha}</div>
              `;
              comentariosContenido.appendChild(comentarioElement);
            });
          } else {
            comentariosContenido.innerHTML = '<div style="text-align: center; padding: 10px;">No hay comentarios aún</div>';
          }
          comentariosLista.style.display = comentariosLista.style.display === 'none' ? 'block' : 'none';
        } else {
          alert('Error al cargar los comentarios');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar los comentarios');
      }
    }
  } catch (error) {
    // El manejo de errores ya está en la función enviarReaccion
    console.error('Error en el manejador de eventos:', error);
  }
});