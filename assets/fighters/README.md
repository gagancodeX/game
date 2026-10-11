# Ryuo character asset

Place the **original Ryuo rigged GLB** at:

`assets/fighters/ryuo.glb`

The game loader already looks for this exact relative path when Ryuo is selected. The file must be a binary glTF 2.0 (.glb) with:
- A skinned humanoid mesh and a working skeleton/skin weights.
- Embedded textures/materials (no external texture paths).
- Animation clips in the same GLB. Clip names should include one of these keywords so the current controller can recognize them:
  - `idle` or `stand`
  - `walk`, `run`, or `move`
  - `jump`
  - `punch`, `attack`, or `hit`
  - `kick`
  - `guard` or `block`
  - `special` or `ultimate`

## Important

The GLB is intentionally **not committed yet**. A model must be supplied/exported and checked before it can be called the original Ryuo character. The loader keeps the procedural fighter visible if the file is missing or fails to load.

Before publishing an asset, confirm its creator/license permits use and redistribution in this repository. Do not rename an unrelated sample model to Ryuo and describe it as original artwork.
