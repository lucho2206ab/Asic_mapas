import L from "leaflet";
import "leaflet/dist/leaflet.css";

const map = L.map("map").setView([-34.6, -58.4], 13); // coordenadas iniciales

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

// Inicializar el control de capas
const controlCapas = L.control.layers({ "OpenStreetMap": L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png") }).addTo(map);
        
fetch("data/RedRiegoPrimeraZona_wgs84.geojson")
  .then(res => res.json())
  .then(data => {
    const capaCauces = L.geoJSON(data, {
      style: {
        color: "blue",
        weight: 2
      },
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: 6,
          fillColor: "green",
          color: "#000",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        });
      },
      onEachFeature: (feature, layer) => {
        if (feature.properties) {
          layer.bindPopup(
            Object.keys(feature.properties)
              .map(k => `<b>${k}</b>: ${feature.properties[k]}`)
              .join("<br>")
          );
        }
      }
    }).addTo(map);

    controlCapas.addOverlay(capaCauces, "Red de Riego");
  });

// Agregar la nueva capa de parcelario
fetch("data/ParcelarioRioMendoza-DerechoSuperior_wgs84.geojson")
  .then(res => res.json())
  .then(data => {
    const capaParcelario = L.geoJSON(data, {
      style: {
        color: "orange",
        weight: 1,
        fillColor: "orange",
        fillOpacity: 0.1
      },
      onEachFeature: (feature, layer) => {
        if (feature.properties) {
          layer.bindPopup(
            Object.keys(feature.properties)
              .map(k => `<b>${k}</b>: ${feature.properties[k]}`)
              .join("<br>")
          );
        }
      }
    }).addTo(map);

    controlCapas.addOverlay(capaParcelario, "Parcelario");
  });

// Agregar la nueva capa de cauces de riego
