---
title: Hardware Design Guide
---

# HSI Mk1 Hardware Design Guide

This guide defines how we design, document, and manage the hardware for the HoverStop project. It ensures consistency, version control, and collaboration across contributors.

## Units
- All measurements and dimensions must be in **millimeters (mm)**.

## Repository Structure
- All parts and assemblies are stored in the GitHub hardware repository.
- Git is the **single source of truth** for design files and history.

## File Structure
Each part will live in its own folder named with a 5-digit part number:

Example folder structure:

```
/12345/
  ├── 12345-Mounting Bracket.step
  ├── 12345-Mounting Bracket.3mf
  ├── metadata.yaml
  ├── REQUIREMENTS.md  # Recommended: Part-specific requirements
  └── 12345-Mounting Bracket.pdf (drawing)
```

**metadata.yaml** will contain:

```yaml
part_number: "12345" # Must be a 5-digit string matching the folder name
owner: "Engines"
name: "Mounting Bracket Example"
description: "Steel bracket that supports the nozzle stop block"
parent_assembly: "12000" # 5-digit part number of parent or "None"
status: "Release" # See "Status Tags" section for allowed values
part_type: "Machined" # See "Part Types" section for allowed values
primary_source: "https://mcmaster.com/1234"
secondary_source: "https://digikey.com/xyz" # Can be "None yet" or similar if not applicable
cost: "4.25" # Can be a number or string like "TBD"
quantity: 1 # Integer, minimum 1
alternatives:
  - description: "Equivalent part from local supplier"
    source: "https://localvendor.com/part"
contributors:
  - "Engines"
  - "Carpet3"
```

## Part Requirements Documentation (Recommended)
It is highly recommended to include a `REQUIREMENTS.md` file within each part's directory. This file should summarize the key design, functional, physical, and manufacturing requirements for that specific part.

## Drawing Requirements
- Every **part** must have a detailed drawing specifying:
  - Dimensions
  - Tolerances (±0.2mm unless otherwise specified)
  - Critical features (holes, mounting surfaces, alignment interfaces)
- Every **assembly** must also include:
  - A complete exploded or assembled view drawing
  - Fastener and hardware BOM (bill of materials)

## General Design Guidance
- Standardize on **DSUB connectors with crimped terminals** as the primary option (solder cup as an alternative).
- Use **white 26AWG hook-up wire** with heatshrink labels for harnesses.
- Avoid reinventing the wheel—reuse existing parts when practical.
- Use standard hardware from the shared Bitkit whenever possible.
- Off-the-shelf parts must include supplier info in metadata.

## Communication
- All major changes, releases, and decisions are posted in Discord.
- Thread-based discussions encouraged per part or topic.
- New part numbers and assignments are coordinated via GitHub or Discord.
