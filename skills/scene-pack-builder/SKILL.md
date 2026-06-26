---
name: scene-pack-builder
description: Build, validate, and preview standardized interactive scene packs for 2D sand-animation workflows. Use when Codex needs to create scene asset libraries with backgrounds, foreground occlusion layers, props, anchors, action templates, ComfyUI-generated assets, or scene.yaml files for AE/Animate/Remotion animation execution.
---

# Scene Pack Builder

## Purpose

Create scene packs that let animation agents place characters, props, cameras, and interactions by named anchors instead of guessing pixel positions from a flat background.

Use this skill before animation production when scenes need sitting, picking up objects, handing over props, entering doors, close-ups, foreground occlusion, or reusable multi-angle backgrounds.

## Output Contract

Create one folder per scene:

```text
scene_<domain>_<number>/
  scene.yaml
  backgrounds/
  layers/
  props/
  masks/
  previews/
```

Every pack must include:

- `scene.yaml` with `scene_id`, `format`, `backgrounds`, `layers`, `anchors`, `props`, and `supported_actions`.
- At least one wide background.
- Multi-framing support for important interactions: `wide`, `medium` or cropped action view, and `close_<target>` / `insert_<target>` backgrounds for doors, tables, screens, containers, signs, or key props.
- Named character anchors in normalized coordinates (`x`, `y`, `scale`).
- Named prop anchors for interactable objects.
- Foreground layers when a character must appear behind furniture or architecture.
- Preview images for at least `wide` and each important interaction.

## Workflow

1. Read the user request and choose a scene domain such as classroom, street, office, room, shop, vehicle, or fantasy hall.
2. Create or import assets:
   - Use existing local assets when available.
   - Use ComfyUI only as an asset generator, not as the animation logic.
   - Keep generated assets in the pack folder, not mixed into unrelated libraries.
   - For ComfyUI API generation, run `scripts/comfyui_queue_workflow.py`.
   - Register selected generated images with `scripts/register_asset.py`.
3. Write `scene.yaml` using the schema in `references/scene-pack-schema.md`.
4. Generate previews:
   - Run `scripts/build_preview.py <scene-pack> --preview all`.
   - For demo packs, run `scripts/scaffold_demo_pack.py <output-dir> --asset-root <public-asset-root>`.
5. Validate:
   - Run `scripts/validate_scene_pack.py <scene-pack>`.
   - Fix missing files, invalid anchors, or unsupported actions before handing the pack to animation.
6. For animation handoff, reference anchors and actions in shot files instead of hardcoding positions.

## Cinematic Coverage Requirements

Scene packs are not just backgrounds. They must support shot language.

- Provide close/insert assets for every important interaction target: table top, door handle, fridge shelf, TV screen, phone screen, signboard, weapon, food, drawer, chair, counter, or document.
- Provide prop states for interactions: before/contact/after, such as `closed/open`, `table/hand/close`, `empty/filled`, `off/on`.
- Provide hand-ready or contact-ready prop variants when possible. If not possible, mark the action template as requiring a hand proxy or object-only insert.
- Provide at least one foreground occlusion layer for sitting, table, counter, or doorway shots.
- Preview every important action from at least two framings: a spatial wide/medium and an insert/closeup.
- If only a single flat wide image exists, mark the pack as `coverage: prototype` and do not use it for interaction-heavy production shots without cropped inserts.

## ComfyUI Integration

Read `references/comfyui-integration.md` when the user wants generated backgrounds, transparent props, multi-angle scenes, style consistency, or API integration with a local ComfyUI server.

Read `references/style-normalization.md` when ComfyUI output needs to match an existing material library or when deciding whether to replace, supplement, or reject generated assets.

ComfyUI should produce raw candidate assets. This skill must still normalize filenames, folder placement, anchors, occlusion layers, and previews.

Typical flow:

```bash
python scripts/comfyui_queue_workflow.py workflow_api.json \
  --output-dir projects/scene-packs/scene_demo_school_01/incoming/comfyui \
  --prefix classroom_wide \
  --prompt "2D cutout animation school hallway, 1920x1080, no characters" \
  --wait

python scripts/register_asset.py projects/scene-packs/scene_demo_school_01 \
  projects/scene-packs/scene_demo_school_01/incoming/comfyui/classroom_wide_01.png \
  --kind background --key wide --resize-1080p
```

## Naming Rules

- Use stable English IDs for folders and YAML keys: `scene_classroom_01`, `stand_left`, `desk_phone`.
- Use human-readable Chinese labels inside YAML when useful: `name: 教室`.
- Keep asset paths relative to `scene.yaml`.
- Avoid spaces in filenames.
- Use `wide`, `medium`, `close_<target>` for background keys.
- Use `<prop>_<state>.png` for prop variants, for example `phone_table.png` and `phone_hand.png`.

## Handoff Example

Animation shot files should call the scene pack like this:

```yaml
scene_pack: projects/scene-packs/scene_demo_school_01/scene.yaml
background: wide
camera: push_to_anchor
actors:
  kana:
    state: sit
    anchor: sit_chair_1
props:
  phone:
    state: hand
    anchor: kana.hand_r
action:
  name: pick_up
  actor: kana
  prop: phone
  from: desk_phone
  to: kana.hand_r
```

The animation executor should resolve these names through `scene.yaml` and action templates.

## Style Gate

- Do not directly replace a production asset with a generated asset unless it matches the active style baseline.
- Keep exploratory ComfyUI outputs in `incoming/comfyui` or under non-production keys such as `comfy_school_wide`.
- Promote a generated asset only after previewing it with characters, props, and foreground layers.
- Prefer reference-guided generation over pure text-to-image when the user needs consistency with an existing library.
