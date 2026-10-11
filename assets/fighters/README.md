# Ryuo character asset

The repository includes a Blender generator at `tools/create_ryuo.py`. It creates an original stylized Ryuo mesh, humanoid armature, materials, and starter animation actions, then exports `assets/fighters/ryuo.glb`.

## Generate the GLB

1. Install Blender 4.x: https://www.blender.org/download/
2. From the repository root, run:

   ```bash
   blender --background --python tools/create_ryuo.py
   ```

3. Confirm that `assets/fighters/ryuo.glb` was created.
4. Open the GLB in Blender or a GLTF viewer and inspect the skeleton, materials, and each animation.
5. Commit the generated binary asset. The static site can then serve it from `/assets/fighters/ryuo.glb`.

## Verification status

The generator script is committed, but the GLB binary is **not generated or committed yet** because Blender is not available in the current execution environment. Do not treat the character as integrated until the binary exists, animation names and rigging are verified in a GLTF viewer, and the deployed browser console confirms successful model loading.

The current loader recognizes animation clip names containing these terms: `idle`/`stand`, `walk`/`run`/`move`, `jump`, `punch`/`attack`/`hit`, `kick`, `guard`/`block`, and `special`/`ultimate`.

Inspect and correct the generated rig, skin weights, and animations before calling it production-ready. Only use assets with licenses that permit redistribution.
