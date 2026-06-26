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

## 2026-06-26 UI and Scene-State Asset Expansion

Added a second asset layer for short-drama information delivery and scene-state changes. This improves animation variety without requiring complex character motion.

New deterministic UI/state assets generated by scripts/create_school_demo_assets.py:

`	ext
projects/scene-packs/scene_demo_school_01/props/
  order_popup.png
  warning_popup.png
  dialogue_bubble_left.png
  dialogue_bubble_right.png
  reaction_exclaim.png
  reaction_question.png
  speed_lines.png
  blackboard_insert.png
  door_insert.png

projects/scene-packs/scene_demo_school_01/backgrounds/
  close_blackboard.png
  close_door.png
`

New scene pack props:

- ui_popup: order, warning
- dialogue_bubble: left, right
- 
eaction_mark: exclaim, question, speed
- environment_insert: blackboard, door

New anchors:

- ui_center
- ui_top_right
- ubble_left
- ubble_right
- 
eaction_left
- 
eaction_right
- lackboard_center
- door_close_center

New action templates:

- show_order_popup
- show_warning_popup
- show_dialogue
- 
eaction_pop
- speed_emphasis
- inspect_blackboard
- inspect_door

New preview coverage:

`	ext
preview_ui_states.png
preview_dialogue.png
preview_warning.png
preview_inspect_blackboard.png
preview_inspect_door.png
school_ui_state_contact_sheet.png
`

Validation status after this pass:

`	ext
OK: scene_demo_school_01 is valid
Checked 43 referenced assets and 23 anchors
`

Workflow note: UI/state overlays are a high-leverage way to make sand-animation scenes feel more dynamic. They should be used for order notifications, rule reveals, warnings, comedy reactions, and fast emphasis cuts before investing in harder limb animation.

## 2026-06-26 Fantasy Hall Scene Pack

Added a second complete scene pack to expand beyond the school test environment:

`	ext
projects/scene-packs/scene_fantasy_hall_01/
`

Purpose: support the original comedy-fantasy delivery story with a demon-king hall, portal entry, meal delivery, magic order reading, payment handoff, and warning beats.

Generated deterministic assets with:

`	ext
scripts/create_fantasy_hall_scene_pack.py
`

Scene pack contents:

- backgrounds: wide, medium, close_throne, close_portal, close_table
- foreground layers: 	hrone_front, 	able_front, portal_frame_front
- props: meal_box, magic_scroll, coin, portal, magic_warning, sword
- anchors: 13 named staging points
- supported actions: 10

Key action templates:

- enter_from_portal
- deliver_meal
- 
ead_magic_order
- hand_over_coin
- open_portal
- show_magic_warning
- sit_throne
- draw_sword

Preview coverage:

`	ext
preview_wide.png
preview_props.png
preview_deliver_meal.png
preview_portal_warning.png
preview_magic_order_close.png
fantasy_hall_props_contact_sheet.png
`

Validation status:

`	ext
OK: scene_fantasy_hall_01 is valid
Checked 20 referenced assets and 13 anchors
`

Asset strategy note: this pack is intentionally deterministic/PIL-generated rather than ComfyUI-generated. The goal is stable staging and action control first; final art can be replaced later while keeping the same anchors, prop IDs, and action templates.

## 2026-06-26 City Street Scene Pack

Added a third complete scene pack for the real-world opening of the delivery story:

`	ext
projects/scene-packs/scene_city_street_01/
`

Purpose: support the ordinary-world delivery beats before the portal transition: rainy street, storefront pickup, phone order, scooter ride, customer-door arrival, and portal/rift event.

Generated deterministic assets with:

`	ext
scripts/create_city_street_scene_pack.py
`

Scene pack contents:

- backgrounds: wide, medium, close_phone, close_store, close_customer_door
- foreground layers: wning_front, us_stop_front
- props: scooter, delivery_bag, phone_order, order_popup, customer_door, portal_rift, 
ain_splash
- anchors: 13 named staging points
- supported actions: 10

Key action templates:

- pick_up_delivery
- check_order
- show_order_popup
- 
ide_scooter
- rrive_customer_door
- open_portal
- enter_portal
- 
ain_loop

Preview coverage:

`	ext
preview_wide.png
preview_props.png
preview_order_popup.png
preview_ride_portal.png
preview_phone_close.png
preview_customer_door.png
city_street_props_contact_sheet.png
`

Validation status:

`	ext
OK: scene_city_street_01 is valid
Checked 17 referenced assets and 13 anchors
`

Workflow note: with scene_city_street_01, scene_fantasy_hall_01, and scene_demo_school_01, the project now has three reusable scene contexts: real-world delivery, fantasy climax, and general dialogue/school-style interaction testing.

## 2026-06-26 Forest Path Scene Pack

Added a fourth complete scene pack for fantasy-route obstacle and encounter beats:

```text
projects/scene-packs/scene_forest_path_01/
```

Purpose: support cursed forest / delivery-road scenes where characters can enter a dangerous path, read signs, clear vines, open a magic barrier, check a delivery map, and negotiate with a dragon through a QR-scan gag.

Generated deterministic assets with:

```text
scripts/create_forest_path_scene_pack.py
```

Scene pack contents:

- backgrounds: wide, medium, close_sign, close_dragon, close_path
- foreground layers: bush_front, vines_front
- props: signpost, vine_trap, magic_barrier, dragon, qr_board, mushroom, fog, delivery_map
- anchors: 12 named staging points
- supported actions: 10

Key action templates:

- enter_forest
- read_sign
- clear_vines
- open_barrier
- encounter_dragon
- scan_qr
- check_map
- fog_reveal

Preview coverage:

```text
preview_wide.png
preview_props.png
preview_obstacles.png
preview_dragon_scan.png
preview_dragon_close.png
preview_map_close.png
forest_path_props_contact_sheet.png
```

Validation status:

```text
OK: scene_forest_path_01 is valid
Checked 19 referenced assets and 12 anchors
```

Workflow note: this pack expands the scene-pack library from dialogue/delivery staging into obstacle-based interaction. It is designed for action-template testing before investing in detailed limb animation or final art replacement.

## 2026-06-26 Takeout Shop Scene Pack

Added a fifth complete scene pack for food pickup, counter dialogue, and small-object interaction beats:

```text
projects/scene-packs/scene_takeout_shop_01/
```

Purpose: support real-world delivery pickup scenes and general shop-counter scenes. This directly addresses the earlier weak point where characters had too few props and scene objects to interact with.

Generated deterministic assets with:

```text
scripts/create_takeout_shop_scene_pack.py
```

Scene pack contents:

- backgrounds: wide, medium, close_counter, close_kitchen, close_menu, close_table
- foreground layers: counter_front, shelf_front, kitchen_window_frame_front
- props: meal_tray, noodle_bowl, receipt, qr_code, drink, delivery_bag, counter_bell, menu_board, steam
- anchors: 16 named staging points
- supported actions: 12

Key action templates:

- ring_bell
- pack_meal
- pick_up_order
- hand_over_meal
- scan_payment
- read_receipt
- inspect_menu
- kitchen_steam
- drink_pickup

Preview coverage:

```text
preview_wide.png
preview_props.png
preview_handover.png
preview_scan_receipt.png
preview_kitchen_steam.png
preview_meal_close.png
preview_menu_close.png
preview_qr_close.png
takeout_shop_props_contact_sheet.png
```

Validation status:

```text
OK: scene_takeout_shop_01 is valid
Checked 27 referenced assets and 16 anchors
```

Workflow note: this pack is a useful template for future "interaction-dense" locations. A good scene pack should not only provide a wide background; it should include foreground occlusion, prop states, close-up inserts, and action templates that let the animation executor move named objects between named anchors.

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
