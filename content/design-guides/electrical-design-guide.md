---
layout: default
title: HSI Mk1 Electrical Design Guide
---

# HSI Mk1 Electrical Design Guide

This guide defines the electrical design standards and practices for the HoverStop project. It ensures consistency, reliability, and maintainability across all electrical systems.

## Wiring Standards
- Use **white 26AWG hook-up wire** for all harnesses.
- Label wires with **heatshrink labels** for clear identification.
- Maintain a small gap between insulation and solder joints to prevent melting into the wire.

## Connector Standards
- Standardize on **DSUB connectors with crimped terminals** as the primary option.
- Use **solder cup DSUB connectors** as an alternative when crimped terminals are not feasible.

## Soldering Guidelines
- Follow the soldering procedures outlined in the [Soldering Wires onto the 23794 Angle Sensor, Hall Effect](../build-guides/turret-soldering/23794-angle-sensor-soldering.md) guide.
- Ensure all solder joints are shiny and show a slightly concave fillet.
- Clean away flux residue after soldering.

## Additional Soldering Guidelines
- For general wire-to-component soldering (e.g., switches, buttons), refer to the [General Wire-to-Component Soldering Guide](../build-guides/wire-to-component-soldering.md).
- Ensure all soldered connections have **12–18mm of heatshrink tubing** applied for insulation and strain relief.

## Harness Design
- Group wires logically and bundle them with cable ties or spiral wrap.
- Avoid sharp bends or excessive strain on wires.
- Test harnesses for continuity and proper connections before installation.

## PCB Design
- Use standard footprints for connectors and components.
- Include test points for critical signals.
- Label all connectors and test points clearly on the silkscreen.

## Wire Lacing
- Follow the [Wire Lacing Guide](../build-guides/wire-lacing-guide.md) for organizing and securing wire bundles.
- Use lacing cord as per FAA AC 43.13-1B, Chapter 11 standards.
- Avoid overtightening to prevent damage to wire insulation.

## Testing and Validation
- Perform continuity tests on all harnesses and PCBs.
- Use a multimeter or oscilloscope to verify signal integrity.
- Document all test results and include them in the project repository.

## Communication
- All major changes, releases, and decisions are posted in Discord.
- Thread-based discussions encouraged per part or topic.
- New part numbers and assignments are coordinated via GitHub or Discord.
