# Shot Schema

Use this schema for AE/Remotion sand-animation shots.

## Sequence Header

```yaml
project_id: magic-delivery
sequence_id: climax_60s_test
runtime_seconds: 60
fps: 12
aspect: "16:9"
format:
  width: 1920
  height: 1080
```

Default output is 1920x1080 horizontal. Only use 9:16 when the user explicitly requests vertical video.

## Required Shot Fields

```yaml
shot_id: C01
duration: 5
location: demon_rooftop
beat: "The delivery rider breaks into the demon king's rooftop before the apocalypse countdown ends."
characters: [delivery_guy, demon_king]
action: scooter_enter
expression: determined_sweat
speaker: narrator
dialogue: "The world is ending because of one bad review."
event_id: apocalypse_delivery_arrival
event_type: arrival
shot_pattern: location_establish_to_entrance
ui: countdown
vfx: dust_pop
vfx_reason: "Scooter brakes hard at the end of the entrance."
transition: cut
camera:
  preset: establishing_pan
  framing: wide
  angle: eye_level
  lens: normal
  move: pan
  subject: delivery_guy
  motivation: establish_space
  motion_intensity: 0.35
  focus: delivery_guy
blocking:
  primary_action: enter
  screen_direction: left_to_right
  start_anchor: roof_entry
  end_anchor: roof_center
interaction:
  contact_frame: null
  actor_anchor: null
  prop_anchor: null
  result_state: arrived
assets:
  required: [bg_demon_rooftop, delivery_guy_body, demon_king_body, scooter, countdown_ui]
  optional: [foreground_rooftop_rail, dust_fx]
  fallback: "Use a wide rooftop background plus scooter silhouette; do not add random shake."
```

## Camera Rules

- `camera.preset` must be one of: `establishing_pan`, `push_in`, `pull_back`, `truck_left`, `truck_right`, `over_shoulder`, `insert_closeup`, `reaction_cut`, `static_hold`.
- `camera.framing` must be one of: `wide`, `medium`, `closeup`, `insert`.
- `camera.angle` must be one of: `eye_level`, `high_angle`, `low_angle`, `pov`, `over_shoulder`, `side`, `front`, `insert`.
- `camera.move` must be one of: `cut`, `push_in`, `pull_back`, `pan`, `tilt`, `truck`, `handheld_bump`, `whip`.
- `camera.motivation` is required. Valid motivations include `establish_space`, `reveal_object`, `show_contact`, `show_reaction`, `compress_time`, `emphasize_joke`, and `show_result`.
- Use `static_hold` only when the dialogue, UI, or expression swap carries the shot.
- A 60-second sequence must include at least 14 shots, at least 5 camera/framing/angle categories, at least 3 framing types, and at least 4 insert/closeup shots when props or UI are important.
- Object interactions must use a shot pattern with before/contact/after coverage. Do not show a prop flying across a wide shot as the only interaction.
- Read `cinematic-shot-patterns.md` before designing shots for pickup, phone call, screen discovery, dialogue, meeting, impact, or travel beats.

## VFX Rules

- Use `none` when no clear story reason exists.
- Any non-`none` VFX requires `vfx_reason`.
- Full-screen white/red flashes may last 2-8 frames only.
- Shake is allowed only as a momentary impact accent, never as looping background motion.
- Do not use VFX to compensate for missing assets.

## Validation

Validation should reject missing required fields, unknown action/expression/transition/camera IDs, vertical format unless explicitly allowed, total duration mismatches, unapproved assets for final render, missing `vfx_reason` for active VFX, excessive flash/shake presets, insufficient camera variation, missing camera motivation, missing shot pattern, object interactions without insert/contact coverage, and asset-density gaps.
