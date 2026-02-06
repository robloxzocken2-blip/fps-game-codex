# fps-game-codex

## 3D Printer Simulation

This repository now contains a browser-based 3D printer simulation.

### Run locally

Open `index.html` directly in a browser, or serve this folder with any static file server, for example:

```bash
python3 -m http.server 4173
```

Then visit `http://localhost:4173`.

### Features

- Layer-by-layer model growth animation
- Moving print head with extrusion effect
- Adjustable target layer count, print speed, and infill density
- Runtime metrics for progress, layer count, nozzle temperature, and ETA
