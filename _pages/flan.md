---
layout: archive
title: "Flans 🍮"
permalink: /flan/
author_profile: true
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<p>Voici un aperçu des flans que j'ai dégustés.</p>

<button onclick="toggleMap()" id="map-toggle" style="background: none; border: 1px solid #aaa; border-radius: 20px; padding: 0.4em 1.2em; cursor: pointer; font-size: 0.95em; margin-bottom: 2em;">
  🗺️ Voir sur la carte
</button>

<div id="map-wrapper" style="max-height: 0; overflow: hidden; transition: max-height 0.5s ease; border-radius: 8px;">
  <div id="flan-map" style="height: 350px; border-radius: 8px;margin-bottom: 1em;"></div>
</div>

<script>
var mapInitialized = false;

function toggleMap() {
  var wrapper = document.getElementById('map-wrapper');
  var btn = document.getElementById('map-toggle');
  var isOpen = wrapper.style.maxHeight !== '0px' && wrapper.style.maxHeight !== '';

  if (isOpen) {
    wrapper.style.maxHeight = '0';
    btn.innerHTML = '🗺️ Voir sur la carte';
  } else {
    wrapper.style.maxHeight = '400px';
    btn.innerHTML = '✕ Fermer la carte';
    if (!mapInitialized) {
      mapInitialized = true;
      var map = L.map('flan-map');
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      var flans = [
        {% for flan in site.data.flans %}{% if flan.lat and flan.lng %}
        { name: {{ flan.name | jsonify }}, address: {{ flan.address | jsonify }}, rating: {{ flan.rating }}, lat: {{ flan.lat }}, lng: {{ flan.lng }} }{% unless forloop.last %},{% endunless %}
        {% endif %}{% endfor %}
      ];
      var bounds = [];
      flans.forEach(function(flan) {
        var marker = L.marker([flan.lat, flan.lng]).addTo(map);
        marker.bindPopup('<strong>' + flan.name + '</strong><br>' + flan.address + '<br>Note : ' + flan.rating + '/5');
        bounds.push([flan.lat, flan.lng]);
      });
      setTimeout(function() {
        map.invalidateSize();
        if (bounds.length === 1) { map.setView(bounds[0], 15); }
        else if (bounds.length > 1) { map.fitBounds(bounds, { padding: [40, 40] }); }
      }, 300);
    }
  }
}
</script>

<script>
var map = L.map('flan-map');
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var flans = [
  {% for flan in site.data.flans %}{% if flan.lat and flan.lng %}
  { name: {{ flan.name | jsonify }}, address: {{ flan.address | jsonify }}, rating: {{ flan.rating }}, lat: {{ flan.lat }}, lng: {{ flan.lng }} }{% unless forloop.last %},{% endunless %}
  {% endif %}{% endfor %}
];

var bounds = [];
flans.forEach(function(flan) {
  var marker = L.marker([flan.lat, flan.lng]).addTo(map);
  marker.bindPopup('<strong>' + flan.name + '</strong><br>' + flan.address + '<br>Note : ' + flan.rating + '/5');
  bounds.push([flan.lat, flan.lng]);
});

if (bounds.length === 1) {
  map.setView(bounds[0], 15);
} else if (bounds.length > 1) {
  map.fitBounds(bounds, { padding: [40, 40] });
}
</script>

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5em;">

{% for flan in site.data.flans %}
<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1.5em;">

  <h2 style="margin-top: 0;">{{ flan.name }}</h2>

  <p style="color: #666; margin: 0.2em 0;">📍 {{ flan.address }}</p>
  <p style="color: #666; margin: 0.2em 0;">🗓️ {{ flan.date }}</p>

  {% if flan.photo %}
  <img src="{{ flan.photo }}" alt="{{ flan.name }}" style="max-width: 100%; max-height: 300px; border-radius: 6px; margin: 1em auto; display: block;">
  {% endif %}

  <p>{{ flan.description }}</p>

  <p><strong>Note:</strong> {{ flan.rating }}/5</p>
  {% if flan.prix %}<p style="margin-bottom: 0;"><strong>Prix:</strong> {{ flan.prix }}€</p>{% endif %}

</div>
{% endfor %}

</div>
