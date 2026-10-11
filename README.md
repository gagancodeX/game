# WORLD FIGHTERS: Legends Unleashed
Render-ready browser 3D fighting-game prototype using Three.js.

## Deploy
This repo is a static site. On Render choose **New + → Static Site**, connect this repository, set build command empty, publish directory `.`, then deploy. A `render.yaml` Blueprint is also included.

## Controls
Keyboard: A/D move, W jump, J punch, K kick, L special. Mobile: on-screen controls.
Choose from six original fighter concepts with elemental themes.

## Scope
This is a browser 3D fighting-game prototype with a procedurally assembled neon arena, fighter fallback meshes, lighting, particles, HUD and basic AI. The optional GLTFLoader and animation-state controller are wired for Ryuo. The actual `assets/fighters/ryuo.glb` model is not included yet, so the live build continues to use the procedural fighter until a properly licensed, rigged GLB with compatible animation clips is added. This is not a finished AAA game; custom character art, tuned combat animation timing, audio, online multiplayer and broad device QA remain future work. Three.js and the optional GLB loader load from CDNs, so internet access is required.
