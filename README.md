# AI_ANIMATRION

AI_ANIMATRION is a local workflow project for producing low-cost 2D sand-animation style shorts with reusable assets, scene packs, Remotion previews, AE scripts, and ComfyUI-assisted material generation.

## Current Direction

The project is moving toward a stable animation executor workflow:

1. Write scripts, shot lists, and action descriptions as structured data.
2. Use standardized scene packs instead of asking an AI model to guess positions.
3. Store backgrounds, foreground occlusion layers, props, anchors, and action templates in `scene.yaml`.
4. Use ComfyUI as an asset factory for missing backgrounds, props, close-ups, and style variants.
5. Use Remotion/MP4 previews for fast validation.
6. Use After Effects and, later, Adobe Animate as editable production layers.

## Important Folders

```text
project/                         Legacy sample story/config files
projects/magic-delivery/          Original comedy fantasy short workflow
projects/scene-packs/             Standardized scene packs
public/免费素材库/                Curated free material library used by previews
skills/                           Local workflow skills and references
src/                              Remotion compositions
scripts/                          Validation, render, and AE generation scripts
ae/                               Generated AE JSX scripts
```

Raw downloaded material libraries, render exports, and temporary ComfyUI candidates are intentionally ignored by Git.

## Scene Pack Workflow

The active scene-pack skill is:

```text
skills/scene-pack-builder/SKILL.md
```

Typical validation:

```powershell
python skills\scene-pack-builder\scripts\validate_scene_pack.py projects\scene-packs\scene_demo_school_01
```

Build scene previews:

```powershell
python skills\scene-pack-builder\scripts\build_preview.py projects\scene-packs\scene_demo_school_01 --preview all
```

Check ComfyUI:

```powershell
python skills\scene-pack-builder\scripts\check_comfyui_setup.py --root D:\ComfyUI_windows_portable
```

## Remotion Commands

```powershell
npm run validate
npm run studio
npm run render
npm run render:magic
npm run render:an-ae
npm run render:state-machine
```

## AE Output

AE scripts live in:

```text
ae/
```

Run the JSX script inside After Effects through `File > Scripts > Run Script File...`; importing a JSX into the project panel will only show it as a file asset and will not execute it.

## Current Notes

See the full status log:

```text
AI_ANIMATION_WORKFLOW_STATUS.md
```

The current conclusion is that ComfyUI is useful for filling asset gaps, especially simple props and style variants. Exact UI/device props such as phones should use references, existing assets, vector/manual material, or img2img rather than pure txt2img.
