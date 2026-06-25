# ComfyUI Integration

Use ComfyUI as an asset factory for scene packs. Do not use it as the source of animation timing, anchors, or action logic.

## Best Uses

ComfyUI is useful for:

- Full backgrounds: `wide`, `medium`, and close-up views.
- Props with transparent backgrounds.
- Matching style variants for the same room or object.
- Foreground occlusion pieces such as desk fronts, chair fronts, counters, doors, and windows.
- Close-up insert images for phone screens, paper, books, paintings, food, and magic items.

## Asset Prompt Pattern

For a scene pack, generate assets as a batch with shared style terms:

```text
2D cutout animation background, clean anime line art, flat readable shapes,
1920x1080, no characters, consistent lighting, simple shadows
```

For transparent props:

```text
single object, solid hot magenta chroma key background,
2D cutout animation prop, clean outline, centered,
no hand, no character, no text
```

Prefer a high-saturation chroma key background over white. White backgrounds can erase white props such as books, paper, cups, and phone highlights during alpha extraction. If the object itself becomes too close to the key color, change the key color and regenerate.

For occlusion layers:

```text
front part of a classroom desk only, transparent background,
2D cutout layer, clean outline, no floor, no wall, PNG alpha
```

## Local API

If ComfyUI is running locally, the default API is usually:

```text
http://127.0.0.1:8188
```

Codex can submit workflow JSON to `/prompt`, poll `/history/{prompt_id}`, and collect generated images from ComfyUI's output folder. Keep workflow JSON outside the scene pack unless it is needed for reproducibility.

Export workflows from ComfyUI with API format enabled. The resulting JSON should be a node mapping whose values contain `class_type` and `inputs`.

## Command-Line Flow

Queue a workflow and download outputs:

```bash
python skills/scene-pack-builder/scripts/comfyui_queue_workflow.py workflow_api.json \
  --server http://127.0.0.1:8188 \
  --output-dir projects/scene-packs/scene_demo_school_01/incoming/comfyui \
  --prefix desk_front \
  --prompt "front part of a classroom desk only, transparent background, 2D cutout layer, PNG alpha" \
  --negative "character, person, full room, blurry, low quality" \
  --wait
```

Override a specific node input when the workflow needs exact control:

```bash
python skills/scene-pack-builder/scripts/comfyui_queue_workflow.py workflow_api.json \
  --output-dir projects/scene-packs/scene_demo_school_01/incoming/comfyui \
  --set 6.text="single smartphone, transparent background, centered PNG alpha" \
  --set 3.seed=12345 \
  --set 5.width=1024 \
  --set 5.height=1024 \
  --wait
```

Register a chosen output into a scene pack:

```bash
python skills/scene-pack-builder/scripts/register_asset.py projects/scene-packs/scene_demo_school_01 \
  projects/scene-packs/scene_demo_school_01/incoming/comfyui/desk_front_01.png \
  --kind layer --key desk_front --layer-group front_character --resize-1080p

python skills/scene-pack-builder/scripts/register_asset.py projects/scene-packs/scene_demo_school_01 \
  projects/scene-packs/scene_demo_school_01/incoming/comfyui/phone_01.png \
  --kind prop --prop phone --variant table --label 手机
```

After registration:

```bash
python skills/scene-pack-builder/scripts/build_preview.py projects/scene-packs/scene_demo_school_01 --preview all
python skills/scene-pack-builder/scripts/validate_scene_pack.py projects/scene-packs/scene_demo_school_01
```

## Recommended Human-in-the-Loop

1. Generate 4-8 candidates per background/prop.
2. Pick one approved style direction.
3. Regenerate missing angles or transparent variants.
4. Remove flat/chroma backgrounds for prop alpha with `scripts/remove_flat_background.py`.
5. Normalize filenames into the scene pack.
6. Write anchors and action templates manually or semi-automatically.
7. Generate previews and inspect occlusion.

## Current Project Policy

For the sand-animation workflow in `D:/短剧`, ComfyUI is currently a gap-filling asset generator, not the replacement source for the whole free library.

Use this intake path:

```text
incoming/comfyui/raw
  -> visual review
  -> style normalization
  -> selected
  -> register_asset.py
  -> build_preview.py
  -> validate_scene_pack.py
```

Prefer reference-guided workflows using approved library assets such as `public/免费素材库/背景/旧学校.png` when generating matching backgrounds, close-ups, or prop variants.

## Common Failures

- **Different camera geometry between wide and close-up views**: acceptable for cutaway shots, not for continuous camera moves.
- **Props fused into backgrounds**: regenerate as isolated transparent props.
- **Chair/table cannot occlude actors**: regenerate or manually cut a `front_character` layer.
- **Object scale varies wildly**: fix in `scene.yaml` with prop scale hints, or regenerate centered props.
- **AI invents hidden parts**: prefer simple objects and simple camera angles for reusable packs.
- **Single prop becomes a collection**: regenerate with `exactly one`, stronger negatives such as `multiple objects`, or use a reference image/img2img.
- **Screen/device props become abstract panels**: use reference-guided generation or existing material first. Pure txt2img is less reliable for UI-like objects.
- **Background removal damages the object**: avoid white backgrounds, use chroma key, and ensure the object color differs from the key color.

## Practical Rule

If a scene requires physical contact, the pack needs both:

- an anchor (`desk_phone`, `sit_chair_1`, `door_handle`);
- an asset layer or prop variant (`phone_hand`, `chair_front`, `door_open`).

Without both, the animation executor will guess and the result will drift.
