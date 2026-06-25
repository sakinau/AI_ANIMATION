# AI-Controlled Animation State Machine

Use a state machine layer when character motion must be stable and repeatable.

## Principle

AI should not animate raw positions frame by frame. AI should output state changes, timing, intensity, target, and blocking intent. The runtime plays approved animation clips.

```text
script beat
  -> intent/template
  -> state timeline
  -> runtime clips
  -> short transparent render
  -> AE composite
```

## Character State Machine

```yaml
character_id: wukong_proxy
runtime: remotion_sim # spine | rive | animate | unity | ae_precomp
states:
  idle:
    clip: idle
    loop: true
    pose: idle
  talk:
    clip: talk
    loop: true
    pose: idle
    mouth: talk
  point:
    clip: point
    loop: false
    pose: point
  shock:
    clip: shock
    loop: false
    pose: idle
    expression: shocked
  attack:
    clip: attack
    loop: false
    pose: point
transitions:
  default: 0.12
anchors:
  foot: [0.5, 0.96]
  head: [0.5, 0.18]
  hand_right: [0.68, 0.48]
```

## Shot State Timeline

```yaml
shot_id: S03
duration: 6
camera_template: over_shoulder_pressure
focus_timeline:
  - {time: 0.0, focus: demon_disguise}
  - {time: 2.0, focus: wukong_reaction}
  - {time: 4.2, focus: monk_doubt}
characters:
  wukong:
    track:
      - {time: 0.0, state: idle, x: 0.30, y: 0.78, scale: 0.82}
      - {time: 1.6, state: shock, x: 0.30, y: 0.78, scale: 0.84}
      - {time: 3.0, state: point, x: 0.36, y: 0.78, scale: 0.86}
  demon:
    track:
      - {time: 0.0, state: disguise_talk, x: 0.66, y: 0.76, scale: 0.82}
      - {time: 4.4, state: reveal, x: 0.70, y: 0.74, scale: 0.94}
```

## Runtime Rules

- Only use states listed in the character state machine.
- Never invent a new state during render. Fall back to `idle` and record a validation warning.
- Use state transitions for character acting. Use AE camera and blocking tracks for spatial emphasis.
- Export small clips for reusable acting beats: `shock_3s`, `talk_5s`, `attack_2s`, `reaction_2s`.
- Audience renders must not include state names, runtime labels, file paths, camera IDs, or debug overlays.

## Cost Control

Start with 8-12 states per main character:

- `idle`
- `talk`
- `walk`
- `point`
- `shock`
- `angry_talk`
- `attack`
- `recoil`
- `celebrate`
- `think`

Add states only after they are used by at least 3 shots or clearly serve a repeatable production need.
