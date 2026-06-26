# AI Animation Workflow Status

Updated: 2026-06-25

## Goal

Build a stable low-cost 2D sand-animation workflow where AI plans story, shots, state timelines, scene packs, and asset generation, while runtime tools execute approved animation states instead of guessing frame-by-frame motion.

The target production style is:

- 1920x1080 horizontal video;
- 2D collage / sand-animation;
- character state machines;
- reusable scene packs;
- visible previewable outputs;
- eventual Animate + After Effects handoff;
- Remotion used for fast testing.

## Current Principle

AI should act as:

```text
director / scheduler / scene-pack planner / asset intake assistant
```

not as:

```text
unconstrained frame-by-frame animator
```

The stable unit should be:

```text
scene_pack + character_state_machine + shot_timeline + action_template
```

## Active Skills

### `ae-sand-drama-workflow`

Path:

```text
D:\短剧\skills\ae-sand-drama-workflow
```

Purpose:

- project bible;
- story outline;
- shot YAML/JSON;
- character state machine;
- Animate/AE/Remotion handoff;
- camera and action beat validation;
- 60-second animation tests.

Important references:

- `references/shot-schema.md`
- `references/animate-layer.md`
- `references/state-machine-runtime.md`

Current status:

- state-machine-driven animation preview works;
- Remotion can render 1080p MP4;
- character motion is improved compared with earlier tests;
- face-overlay replacement is temporarily avoided because free-library characters are not face-anchor-safe.

### `scene-pack-builder`

Path:

```text
D:\短剧\skills\scene-pack-builder
```

Purpose:

- create standardized interactive scene packs;
- define backgrounds, foreground occlusion layers, props, anchors, and supported actions;
- use ComfyUI as an asset factory;
- validate scene packs;
- generate preview images for staging and occlusion checks.

Important references:

- `references/scene-pack-schema.md`
- `references/comfyui-integration.md`
- `references/style-normalization.md`

Scripts:

- `scripts/scaffold_demo_pack.py`
- `scripts/validate_scene_pack.py`
- `scripts/build_preview.py`
- `scripts/comfyui_queue_workflow.py`
- `scripts/register_asset.py`
- `scripts/check_comfyui_setup.py`

Current status:

- first scene-pack demo generated and validated;
- ComfyUI API generation is connected;
- generated images can be downloaded, registered, previewed, and validated;
- style normalization rules have been added.

## Tool Stack

### Rendering / Preview

- Remotion
- React / TypeScript
- local runtime at `F:\Animation_AI`
- MP4 render scripts under `D:\短剧\scripts`

### Animation Runtime Direction

Planned / supported layers:

- Adobe Animate: character animation, expression/mouth/action loops;
- After Effects: shot compositing, camera movement, VFX, subtitles, packaging;
- Remotion: fast preview and validation;
- optional future runtimes: Spine, Rive, Unity Animator, AE precomp proxies.

### Asset Generation

ComfyUI portable install:

```text
D:\ComfyUI_windows_portable
```

Server:

```text
http://127.0.0.1:8188
```

Detected GPU:

```text
AMD Radeon RX 9070 GRE
```

Installed checkpoint:

```text
D:\ComfyUI_windows_portable\ComfyUI\models\checkpoints\animagine-xl-4.0-opt.safetensors
```

Model role:

- anime / illustration / 2D material generation;
- useful for background, prop, and visual candidate generation;
- not yet accepted as the final global style.

## Existing Outputs

### State Machine Test Video

Path:

```text
D:\短剧\output\state-machine-kana-rina-60s-test.mp4
```

Source script:

```text
F:\Animation_AI\timeline.json
F:\Animation_AI\src\dialogue-data.ts
```

Status:

- 1920x1080;
- about 60 seconds;
- uses free material library;
- face overlays removed to avoid mismatch.

### Demo Scene Pack

Path:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01
```

Contains:

- `scene.yaml`;
- wide / medium / close_desk backgrounds;
- desk, chair, and door foreground layers;
- phone, book, and cup placeholder props;
- anchor table;
- action templates;
- preview images.

Validation:

```text
OK: scene_demo_school_01 is valid
```

### First ComfyUI Test Asset

Raw output:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\incoming\comfyui\school_bg_test_01.png
```

Registered output:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\backgrounds\comfy_school_wide.png
```

Workflow:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\workflows\animagine_sdxl_background_api.json
```

Status:

- technically successful;
- style is not yet consistent with the existing free library;
- kept under exploratory key `comfy_school_wide`, not promoted to production `wide`.

### First Style-Lock Test

Reference image:

```text
D:\短剧\public\免费素材库\背景\旧学校.png
```

ComfyUI input copy:

```text
D:\ComfyUI_windows_portable\ComfyUI\input\scene_pack_refs\old_school_reference.png
```

Workflow:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\workflows\animagine_sdxl_img2img_stylelock_api.json
```

Generated candidates:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\incoming\comfyui\school_stylelock_038_01.png
D:\短剧\projects\scene-packs\scene_demo_school_01\incoming\comfyui\school_stylelock_055_01.png
```

Registered exploratory asset:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\backgrounds\stylelock_school_wide_055.png
```

Comparison preview:

```text
D:\短剧\projects\scene-packs\scene_demo_school_01\previews\stylelock_comparison.png
```

Conclusion:

- Pure txt2img drifts too much for the current free-library baseline.
- img2img with `denoise: 0.38` best preserves the baseline but changes little.
- img2img with `denoise: 0.55` is the current best candidate for same-style background variants.
- Keep style-locked outputs under exploratory keys until previewed with characters and props.

## Current Material Strategy

Do not replace all assets with ComfyUI output yet.

Short-term policy:

```text
existing free library = production baseline
ComfyUI = gap-filling candidate generator
```

ComfyUI should first generate:

- missing backgrounds;
- close-up inserts;
- foreground occlusion layers;
- props;
- variant views;
- style experiments.

Generated material must pass:

```text
incoming/comfyui/raw
  -> review
  -> style normalization
  -> selected
  -> register_asset
  -> preview
  -> validate
```

## Known Problems

1. Free material library is sparse.
   - few backgrounds;
   - few props;
   - weak scene-character interaction;
   - limited camera angle variety.

2. Face overlay is unstable.
   - character heads and face assets do not share reliable anchors;
   - current workaround is full-pose assets or emotion bubbles/status labels.

3. ComfyUI txt2img style differs from existing material.
   - line density and perspective differ;
   - generated background currently should not be mixed blindly with free-library characters.

4. Scene interaction requires structured packs.
   - sitting, picking objects, handing props, entering doors, and desk occlusion require anchors and foreground layers.

## Technical Direction

### Scene Packs

Every reusable location should become:

```text
scene_<domain>_<id>/
  scene.yaml
  backgrounds/
  layers/
  props/
  masks/
  previews/
  incoming/
  workflows/
```

Required concepts:

- named anchors;
- foreground occlusion;
- prop variants;
- close-up backgrounds;
- supported actions;
- action templates.

### Action Templates

The animation layer should call actions like:

```yaml
action:
  name: pick_up
  actor: kana
  prop: phone
  from: desk_phone
  to: kana.hand_r
```

instead of raw hand-authored coordinates for every shot.

### Style Locking

Next ComfyUI upgrade should move from pure txt2img to reference-guided generation:

- img2img from approved material;
- lineart / Canny control;
- style reference / IPAdapter-like workflow;
- background removal for props;
- post-processing for color and outline consistency.

## 2026-06-25 Prop Generation Test

Completed a first end-to-end prop intake pipeline:

```text
ComfyUI prop workflow
  -> raw chroma/flat-background PNG
  -> remove_flat_background.py
  -> register_asset.py
  -> prop_candidates_comparison.png
  -> scene pack validation
```

Generated and registered exploratory props in:

```text
projects/scene-packs/scene_demo_school_01/props/
  phone_comfy_table.png
  cup_comfy_table.png
  book_comfy_closed.png
```

Preview/contact sheet:

```text
projects/scene-packs/scene_demo_school_01/previews/prop_candidates_comparison.png
```

Findings:

- Simple objects such as cups and closed books are suitable for pure ComfyUI txt2img candidate generation.
- White-background prop generation is unsafe for white objects; it can erase paper/book/cup surfaces during background removal.
- The prop workflow now defaults to hot-magenta chroma key prompts instead of white backgrounds.
- Screen/device props such as phones are unstable with pure txt2img: the model may generate multiple devices or abstract UI panels. For phones, UI screens, paper text, signs, and exact tools, use existing material, reference-guided img2img, or manual/vector assets first.
- `register_asset.py` now uses a scene-level lock to avoid concurrent writes overwriting `scene.yaml` during batch registration.

Validation status:

```text
OK: scene_demo_school_01 is valid
Checked 19 referenced assets and 9 anchors
Skill is valid
```

## 2026-06-26 Scene Pack Asset Expansion

Extended scene_demo_school_01 from a basic desk/phone test pack into a richer interaction test pack.

New deterministic transparent PNG props were generated with scripts/create_school_demo_assets.py:

`	ext
projects/scene-packs/scene_demo_school_01/props/
  phone_close.png
  book_hand.png
  book_close.png
  cup_close.png
  paper_note_table.png
  paper_note_hand.png
  paper_note_close.png
  delivery_bag_floor.png
  delivery_bag_hand.png
  key_table.png
  key_hand.png
  chalk_table.png
  chalk_hand.png
`

New props registered in scene.yaml:

- paper_note: table, hand, close
- delivery_bag: floor, hand
- key: table, hand
- chalk: table, hand
- added close/hand variants for existing phone, book, and cup

New anchors:

- desk_note
- desk_key
- desk_chalk
- loor_delivery_bag
- handoff_mid
- close_insert_center

New or improved action templates:

- 
ead_note
- open_book
- drink
- unlock_door
- deliver_bag
- hand_over
- inspect_close

Preview coverage now includes:

`	ext
preview_props.png
preview_read_note.png
preview_handover.png
preview_inspect_close.png
school_extra_props_contact_sheet.png
`

Validation status after expansion:

`	ext
OK: scene_demo_school_01 is valid
Checked 32 referenced assets and 15 anchors
Skill is valid
`

Implementation note: uild_preview.py now understands ariant_scales, so reusable prop PNGs can keep stable source dimensions while scene previews and animation handoff receive sane per-variant display scale hints.

## Next Operations

1. Build a reference-guided ComfyUI test.
   - Use `public/免费素材库/背景/旧学校.png` as the style/reference source.
   - Generate a school corridor or classroom close-up that better matches the existing library.
   - Status: first img2img style-lock test completed. `denoise: 0.55` is the current best setting among tested candidates.

2. Generate transparent prop candidates.
   - Status: table variants tested for phone/cup/book.
   - Next: generate hand variants only after character hand anchors and grip pose templates are defined.
   - Next: make phone from reference-guided img2img or existing vector/material, not pure txt2img.

3. Add style normalization scripts.
   - Status: flat/chroma background removal script added.
   - Next: add automatic alpha sanity checks and key-color residue detection.
   - Next: add color flatten and outline enhancement.
   - side-by-side comparison preview.

4. Update `scene_demo_school_01`.
   - keep current generated background as exploratory;
   - add selected ComfyUI props only after preview;
   - do not promote generated background to `wide` until style matches.

5. Connect scene pack to animation preview.
   - create a short Remotion test where a character sits, picks up phone, and interacts with desk/foreground occlusion.

6. Later: consider installing or borrowing ideas from SkillsMP.
   - `comfyui-agent-skill-mie`;
   - `comfyui-txt2img`;
   - `comfyui-python-ws-client`;
   - `comfyui-node-installer`.

## Useful Commands

Check ComfyUI:

```powershell
python skills\scene-pack-builder\scripts\check_comfyui_setup.py --root D:\ComfyUI_windows_portable
```

Generate with ComfyUI API:

```powershell
python skills\scene-pack-builder\scripts\comfyui_queue_workflow.py projects\scene-packs\scene_demo_school_01\workflows\animagine_sdxl_background_api.json `
  --server http://127.0.0.1:8188 `
  --output-dir projects\scene-packs\scene_demo_school_01\incoming\comfyui `
  --prefix school_bg_test `
  --wait
```

Register generated asset:

```powershell
python skills\scene-pack-builder\scripts\register_asset.py projects\scene-packs\scene_demo_school_01 `
  projects\scene-packs\scene_demo_school_01\incoming\comfyui\school_bg_test_01.png `
  --kind background --key comfy_school_wide --resize-1080p
```

Preview scene pack:

```powershell
python skills\scene-pack-builder\scripts\build_preview.py projects\scene-packs\scene_demo_school_01 --preview all
```

Validate scene pack:

```powershell
python skills\scene-pack-builder\scripts\validate_scene_pack.py projects\scene-packs\scene_demo_school_01
```
