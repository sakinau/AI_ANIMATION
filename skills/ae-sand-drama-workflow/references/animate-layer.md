# Animate Character Layer

Use Adobe Animate as the character-animation layer. AE should receive finished character animation sequences or editable character precomps, not raw face/mouth swap decisions.

## Folder Contract

```text
projects/<project-id>/
  workflow/an_ae_pipeline.yaml
  characters/<character-id>.yaml
  renders/an/<sequence>/<shot-id>/<character-id>/frame-0000.png
  renders/ae/<sequence>/
```

## Character Manifest

```yaml
character_id: delivery_guy
role: protagonist
source_type: png_parts
scale_reference_height: 820
animate:
  fla_path: an/delivery_guy.fla
  export_root: projects/magic-delivery/renders/an
layers:
  body:
    idle: public/asset-path/body-idle.png
    walk: public/asset-path/body-walk.png
    point: public/asset-path/body-point.png
  face:
    neutral: public/asset-path/face-neutral.png
    shocked: public/asset-path/face-shocked.png
    angry: public/asset-path/face-angry.png
  mouth:
    closed: generated
    a: generated
    o: generated
actions:
  talk_hold:
    pose: idle
    expression_cycle: [neutral, shocked, neutral]
    mouth_cycle: [closed, a, closed, o]
  point_talk:
    pose: point
    expression_cycle: [angry, shocked]
    mouth_cycle: [a, closed, o, closed]
```

## Face Normalization

Do not use raw expression PNGs directly. First normalize every expression into a single transparent canvas and one shared coordinate system.

```yaml
face_normalization:
  canvas: [180, 132]
  face_box: [132, 92]
  eye_line_y: 58
  mouth_anchor: [90, 88]
pose_anchors:
  idle:
    left: 121
    top: 116
    width: 142
    height: 104
    eye_line: 48
    mouth_anchor: [70, 78]
  point:
    left: 126
    top: 116
    width: 142
    height: 104
    eye_line: 48
    mouth_anchor: [70, 78]
```

If the face is misaligned, change `pose_anchors`; do not hand-tune individual shot coordinates.

Do not perform face replacement on bodies that already have painted facial features or hair covering the face plane. Those assets need either full-pose expression variants or external emotion bubbles.

## JSFL Automation Goals

- Import body/face/mouth/prop assets into the library.
- Create symbols with stable names.
- Build a timeline with layers in this order: `notes`, `mouth`, `face`, `prop`, `right_arm`, `left_arm`, `head`, `body`, `shadow`.
- Place keyframes from the shot action plan.
- Export transparent PNG sequences per character per shot.

## Remotion Fallback

When Animate is unavailable, simulate the Animate layer:

- Use the same character manifest.
- Use body pose images as the base layer.
- Swap only normalized expression images on frame ranges.
- Pulse or swap simple mouth shapes during dialogue.
- Hide debug labels in audience-facing renders. Show layer labels only in still checks or debug exports.
- Keep this fallback visually honest: label it as `AN_SIM` in metadata, and do not treat it as the final Animate output.
