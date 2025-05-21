---
layout: default
title: Service Documentation Home
---

# Service Documentation

Welcome to the service documentation site. This repository contains troubleshooting guides for service engineers.

## Available Sections

<ul>
  {% assign sections = site.pages | map: 'dir' | uniq | sort %}
  {% for section in sections %}
    {% if section contains '/content/' and section != '/content/' %}
      <li><a href="{{ section | relative_url }}">{{ section | split: '/' | last | replace: '-', ' ' | capitalize }}</a></li>
    {% endif %}
  {% endfor %}
</ul>

## All Guides

<div class="guides-container">
  {% for page in site.pages %}
    {% if page.path contains 'content/' and page.name != 'index.md' and page.name != 'guides.md' %}
    <div class="guide-card">
      <a href="{{ page.url | relative_url }}">
        <h3>{{ page.title }}</h3>
        <div class="guide-meta">
          <span class="guide-type">Guide</span>
        </div>
        <div class="guide-arrow">→</div>
      </a>
    </div>
    {% endif %}
  {% endfor %}
</div>

{% assign guide_count = 0 %}
{% for page in site.pages %}
  {% if page.path contains 'content/' and page.name != 'index.md' and page.name != 'guides.md' %}
    {% assign guide_count = guide_count | plus: 1 %}
  {% endif %}
{% endfor %}

{% if guide_count == 0 %}
<div class="notice">
  <p>No guides available yet. Check back soon or contact the Service Engineering team for assistance.</p>
</div>
{% endif %} 