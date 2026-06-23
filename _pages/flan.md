---
layout: archive
title: "Flans 🍮"
permalink: /flan/
author_profile: true
---

Voici un aperçu des flans que j'ai dégusté.

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div id="flan-map" style="height: 400px; border-radius: 8px; margin: 1.5em 0;"></div>

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

{% for flan in site.data.flans %}
<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1.5em; margin-bottom: 2em;">

  <h2 style="margin-top: 0;">{{ flan.name }}</h2>

  <p style="color: #666; margin: 0.2em 0;">
    📍 {{ flan.address }} &nbsp;·&nbsp; 🗓️ {{ flan.date }}
  </p>

  {% if flan.photo %}
  <img src="{{ flan.photo }}" alt="{{ flan.name }}" style="max-width: 100%; max-height: 300px; border-radius: 6px; margin: 1em 0; display: block;">
  {% endif %}

  <p>{{ flan.description }}</p>

  <p><strong>Note:</strong> {{ flan.rating }}/5</p>
  {% if flan.prix %}<p style="margin-bottom: 0;"><strong>Prix:</strong> {{ flan.prix }}€</p>{% endif %}

</div>
{% endfor %}
