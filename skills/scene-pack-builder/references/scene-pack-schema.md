# Scene Pack Schema

Use `scene.yaml` as the single source of truth for a reusable interactive scene.

## Required Top-Level Fields

```yaml
scene_id: scene_demo_school_01
name: 学校走廊样板
version: 0.1.0
format:
  width: 1920
  height: 1080
backgrounds:
  wide: backgrounds/wide.png
layers:
  background:
    - backgrounds/wide.png
  behind_character: []
  front_character: []
anchors:
  stand_left: {x: 0.30, y: 0.82, scale: 0.85}
props: {}
supported_actions:
  - stand
```

## Coordinates

- `x` and `y` are normalized to the scene format.
- `x: 0` is left edge, `x: 1` is right edge.
- `y: 0` is top edge, `y: 1` is bottom edge.
- Character anchors represent the foot or seated base point.
- Prop anchors represent the visual center unless a `pivot` field says otherwise.

## Layers

Use the layer groups to solve occlusion:

- `background`: full-frame base and distant elements.
- `behind_character`: furniture/back parts behind actors.
- `front_character`: desk fronts, chair fronts, door frames, counters, or railings that cover actors.
- `overlay`: optional effects or UI-like environment pieces.

Example:

```yaml
layers:
  background:
    - backgrounds/wide.png
  behind_character:
    - layers/chair_back.png
    - layers/desk_back.png
  front_character:
    - layers/chair_front.png
    - layers/desk_front.png
```

## Anchors

Minimum recommended anchors:

```yaml
anchors:
  stand_left: {x: 0.30, y: 0.82, scale: 0.85}
  stand_right: {x: 0.66, y: 0.82, scale: 0.85}
  sit_chair_1: {x: 0.44, y: 0.79, scale: 0.82, facing: right}
  desk_center: {x: 0.52, y: 0.60, scale: 1.0}
  door_entry: {x: 0.84, y: 0.82, scale: 0.78}
```

Use optional `facing`, `z_hint`, and `notes` fields when helpful.

## Props

Props must reference one or more asset variants:

```yaml
props:
  phone:
    label: 手机
    variants:
      table: props/phone_table.png
      hand: props/phone_hand.png
      close: props/phone_close.png
    default_anchor: desk_phone
    pivot: center
```

Recommended prop variants:

- `table`: resting on a surface.
- `hand`: already rotated/scaled for hand-held use.
- `close`: larger insert shot.
- `open` / `closed`: books, doors, boxes.
- `front` / `side`: angle variants.

## Actions

`supported_actions` declares what the pack can perform. `action_templates` may define default timing and anchor use.

```yaml
supported_actions:
  - stand
  - sit
  - pick_up
  - put_down
  - hand_over
  - enter_from_door
  - inspect_close

action_templates:
  pick_up:
    duration: 1.2
    actor_state_sequence: [reach, grab, hold]
    prop_sequence:
      - {time: 0.0, variant: table, anchor: desk_phone}
      - {time: 0.7, variant: hand, anchor: actor.hand_r}
  sit:
    duration: 1.0
    actor_state_sequence: [stand, bend, sit]
    target_anchor: sit_chair_1
    requires_front_layers: [chair_front]
```

## Quality Checklist

- A preview exists for every declared important action.
- Interactable props have table and hand variants when applicable.
- Sitting or behind-desk actions have foreground occlusion layers.
- Anchors are normalized and within `[0, 1]`.
- Every file path in `scene.yaml` exists relative to the pack.
- `scene.yaml` has no absolute paths.
