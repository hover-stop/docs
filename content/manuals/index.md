---
layout: default
title: Manuals
---

<details markdown="1">
<summary><strong>Document Information</strong></summary>

| Document Title | HoverStop Manuals Overview |
| :---- | ----- |
| **Document Number** | 0006 |
| **Version Number** | 1.0 |
| **Effective Date** | 3 May 25 |
| **Prepared By** | HoverStop Documentation Team |
| **Reviewed By** |  |
| **Approved By** |  |
| **Next Review Date** | 3 Jun 25 |
| **Location** | GitHub - hover-stop/docs |

| Version | Date | Description of Change | Changed By |
| ----- | ----- | ----- | ----- |
| 1.0 | 3 May 25 | Initial release | HoverStop Docs Team |

</details>

# Manuals

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