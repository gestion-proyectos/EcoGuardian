document.addEventListener("DOMContentLoaded", function () {
    const map = L.map("map").setView([6.1495, -75.6190], 16);
    const listaDiv = document.getElementById("ruta-lista");
    const rutasEnMapa = {};
    const checkboxes = [];
   
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "© OpenStreetMap"
    }).addTo(map);
   
    fetch("/api/rutas_recomendadas")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        data.features.forEach((feature, index) => {
          const nombre = feature.properties?.name || `Ruta ${index + 1}`;
          const criticidad = feature.properties?.criticidad?.toLowerCase() || "desconocida";
   
          let color = "gray";
          if (criticidad === "baja") color = "green";
          else if (criticidad === "media") color = "orange";
          else if (criticidad === "alta") color = "red";
   
          const rutaLayer = L.geoJSON(feature, {
            style: { color: color, weight: 5 },
            onEachFeature: function (feat, layer) {
              const coords = feat.geometry?.coordinates;
              if (Array.isArray(coords) && coords.length >= 2) {
                const inicio = coords[0];
                const fin = coords[coords.length - 1];
   
                L.marker([inicio[1], inicio[0]]).addTo(map).bindPopup(`Inicio de ${nombre}`);
                L.marker([fin[1], fin[0]]).addTo(map).bindPopup(`Fin de ${nombre}`);
              }
   
              layer.bindPopup(`<b>${nombre}</b><br>Criticidad: ${criticidad}`);
            }
          }).addTo(map);
   
          rutasEnMapa[nombre] = rutaLayer;
   
          const checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.checked = true;
          checkbox.className = "form-check-input";
          checkbox.dataset.ruta = nombre;
   
          checkbox.addEventListener("change", function () {
            if (this.checked) {
              rutasEnMapa[nombre].addTo(map);
            } else {
              map.removeLayer(rutasEnMapa[nombre]);
            }
          });
   
          const label = document.createElement("label");
          label.className = "form-check-label";
          label.innerHTML = `<span class="color-box" style="background:${color}"></span>${nombre}`;
   
          const wrapper = document.createElement("div");
          wrapper.className = "form-check d-flex align-items-center gap-2";
          wrapper.appendChild(checkbox);
          wrapper.appendChild(label);
   
          checkboxes.push(checkbox);
          listaDiv.appendChild(wrapper);
        });
   
        // Botones seleccionar/deseleccionar
        document.getElementById("btn-select-all").addEventListener("click", () => {
          checkboxes.forEach((cb) => {
            cb.checked = true;
            rutasEnMapa[cb.dataset.ruta].addTo(map);
          });
        });
   
        document.getElementById("btn-deselect-all").addEventListener("click", () => {
          checkboxes.forEach((cb) => {
            cb.checked = false;
            map.removeLayer(rutasEnMapa[cb.dataset.ruta]);
          });
        });
      })
      .catch((error) => {
        console.error("❌ Error cargando las rutas:", error);
      });
  });
   