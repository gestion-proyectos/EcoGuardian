// Función para inicializar el mapa
function initMap() {
    if (document.getElementById('map')) {
        var map = L.map('map').setView([40.416775, -3.703790], 6);
        
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
    }
}

// Función para validar formularios
function validateForm() {
    var password = document.getElementById('password');
    var confirmPassword = document.getElementById('confirm_password');
    
    if (password && confirmPassword) {
        if (password.value !== confirmPassword.value) {
            alert('Las contraseñas no coinciden');
            return false;
        }
    }
    return true;
}

// Inicializar cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    
    // Agregar validación a formularios
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            }
        });
    });
});