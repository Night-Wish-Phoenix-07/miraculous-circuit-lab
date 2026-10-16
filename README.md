# Miraculous Circuit Lab

A circuit simulator in Python with a 3D view and Miraculous themes
(Ladybug and Cat Noir). Built as a Tinkercad alternative for learning
2nd-year ECE circuits.

## Features
- DC circuit solver (Modified Nodal Analysis) with resistors, voltage and current sources
- 3D scene using Ursina, where LED brightness comes from the solved current
- Two themes: press L for Ladybug, C for Cat Noir

## Run it
pip install -r requirements.txt
python lab3d.py

## Controls
- Right mouse drag: rotate
- Scroll: zoom
- L / C: switch theme

## Roadmap
- Capacitor and inductor (transient analysis)
- Diode, transistor, op-amp
- Drag and drop components
