---
layout: default
title: Design Guides
---

# Design Guides

<div class="guides-container">
  {% assign section_pages = site.pages | where: "dir", page.dir | sort: "nav_order" %}
  {% for child in section_pages %}
    {% if child.name != 'index.md' %}
    <div class="guide-card">
      <a href="{{ child.url | relative_url }}">
        <h3>{{ child.title }}</h3>
        <div class="guide-meta">
          <span class="guide-type">Guide</span>
        </div>
        <div class="guide-arrow">→</div>
      </a>
    </div>
    {% endif %}
  {% endfor %}
</div> 