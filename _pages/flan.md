---
layout: archive
title: "Flans 🍮"
permalink: /flan/
author_profile: true
---

Voici un aperçu des flans que j'ai dégusté. 

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
