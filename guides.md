---
layout: default
title: Service Guides
permalink: /guides/
---

# Service Guides

Browse all available troubleshooting guides for service engineers. These guides are designed to help diagnose and resolve common issues.

## All Guides

<div class="guides-container">
  {% for page in site.pages %}
    {% if page.path contains 'guides/' and page.name != 'index.md' and page.name != 'guides.md' %}
    <div class="guide-card">
      <a href="{{ page.url | relative_url }}">
        <h3>{{ page.title }}</h3>
        <div class="guide-meta">
          <span class="guide-type">Troubleshooting Guide</span>
        </div>
        <div class="guide-arrow">→</div>
      </a>
    </div>
    {% endif %}
  {% endfor %}
</div>

{% assign guide_count = 0 %}
{% for page in site.pages %}
  {% if page.path contains 'guides/' and page.name != 'index.md' and page.name != 'guides.md' %}
    {% assign guide_count = guide_count | plus: 1 %}
  {% endif %}
{% endfor %}

{% if guide_count == 0 %}
<div class="notice">
  <p>No guides available yet. Check back soon or contact the Service Engineering team for assistance.</p>
</div>
{% endif %} 