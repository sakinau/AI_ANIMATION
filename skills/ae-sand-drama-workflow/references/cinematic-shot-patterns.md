# Cinematic Shot Patterns

Use this reference when a beat contains physical action, object interaction, discovery, dialogue, or location change. Do not stage the whole beat from one front-facing master shot.

## Principle

Convert each story beat into a shot pattern before writing final shot YAML:

```yaml
beat: "Xiaoming opens the fridge and takes eggs and milk."
event_type: object_pickup
shot_pattern: object_pickup_sequence
```

The pattern decides camera variety, insert shots, action granularity, and edit rhythm. The renderer then executes short, simple shots.

## Event-To-Shot Workflow

Prefer this sequence for production:

1. Write a compact event file, for example `shots/<sequence>_events.json`.
2. For each event, set `event_type`, `shot_pattern`, `scene_pack`, `background`, phase-specific `actions`, `dialogue`, `subjects`, and optional `blocking` / `interaction`.
3. Add or update `subject_registry` so every subject and anchor used by the shots can be resolved.
4. Add or update `action_registry` so every shot action can be executed by a scene pack, renderer, runtime clip/state, or fallback.
5. Expand the event file:

```powershell
python scripts\expand_cinematic_beats.py projects\<project-id>\shots\<sequence>_events.json --output projects\<project-id>\shots\<sequence>_generated.json
```

6. Validate the generated shot list:

```powershell
python scripts\validate_cinematic_shots.py projects\<project-id>\shots\<sequence>_generated.json
```

7. Render Remotion/AE from the generated shot list, not from a hand-written one-off long shot list.

The event file is the creative control surface; the generated shot list is the execution contract.

## Renderer Contract

The renderer must treat each generated shot as a cinematic instruction, not as a suggestion to be merged back into a master shot.

Execution order:

1. Read `purpose`.
2. Read `edit.transition`, `edit.continuity`, and `edit.reason`.
3. Read `camera.subject`, `camera.angle`, `camera.framing`, and `camera.move`.
4. Resolve scene-pack background, foreground, prop state, and anchor data.
5. Execute the matching template for that purpose.
6. Use action-specific custom code only when the generic purpose template cannot express the shot.

Required renderer behavior:

- `contact` means show contact or near-contact in close framing.
- `screen_insert` means the screen/sign/UI information must be readable.
- `reaction_close` means the audience should see the character response, not another wide shot.
- `result_insert` means the prop or state after the action must be visible.
- `location_establish` means show geography or signage before cutting into closer shots.

Never collapse an expanded shot group back into one front-facing master camera. If an asset is missing, select a declared fallback such as a crop insert, hand proxy, object-only insert, reaction icon, or text-safe UI insert.

## Edit Continuity

Each generated shot must include:

```json
{
  "edit": {
    "transition": "insert_cut",
    "continuity": "look_to_screen",
    "reason": "make screen information readable"
  }
}
```

Recommended transitions:

- `scene_start`: first shot of a sequence or location.
- `context_cut`: cut to establish actor context before a discovery.
- `insert_cut`: cut into readable prop, screen, sign, UI, or object detail.
- `action_match_cut`: cut on an action path, usually hand/object contact.
- `pov_cut`: cut from character/contact to what the character sees.
- `reaction_cut`: cut from information/object/action to character reaction.
- `speaker_cut` / `reverse_cut`: dialogue and phone-call speaker changes.
- `result_cut`: show the post-action state.
- `split_screen_bridge`: bridge two speakers or places through a designed layout.
- `scene_cut` / `time_cut`: explicit location or time jump.

Validation target:

- Scene-pack changes require `scene_cut`, `time_cut`, `graphic_match`, or `split_screen_bridge`.
- Insert/contact/result purposes require insert/action/pov/result transitions.
- Reaction and speaker purposes require reaction/speaker/reverse/result transitions.
- Background changes inside one scene pack must be motivated by insert, context, result, reaction, POV, or action-match editing.

## Subject Registry

The event file should include a top-level `subject_registry`. This makes spatial references auditable before rendering:

```json
{
  "subject_registry": {
    "xiaoming": {"type": "actor"},
    "xiaoming_hand_r": {"type": "actor_anchor", "actor": "xiaoming", "anchor": "hand_r"},
    "phone": {"type": "prop", "scene_pack": "scene_customer_room_01", "prop": "phone", "anchor": "table_phone"},
    "tv": {"type": "scene_anchor", "scene_pack": "scene_customer_room_01", "anchor": "tv_center", "background": "close_tv"},
    "fridge_handle": {"type": "temporary_prop", "fallback": "test-only fridge handle insert"}
  }
}
```

Validation rules:

- `camera.subject` must exist in `subject_registry` or in the shot's `scene_pack` as a background, prop, or anchor.
- `scene_pack`, `background`, `prop`, `variant`, and `anchor` references must exist in `scene.yaml`.
- Non-dotted `blocking.start_anchor`, `blocking.end_anchor`, and `interaction.prop_anchor` must exist in `scene.yaml` or be declared as `actor_anchor` / `temporary_anchor`.
- Temporary subjects must include a `fallback` note so missing production assets stay visible.

## Action Registry

The event file should include `action_registry` whenever actions are not direct scene-pack actions:

```json
{
  "action_registry": {
    "pick_remote": {"type": "scene_action", "scene_pack": "scene_customer_room_01", "action": "pick_remote"},
    "caller_close": {"type": "render_action", "handler": "CinematicInteractionTest.caller_close", "reason": "test-only caller closeup"},
    "hero_talk_loop": {"type": "runtime_action", "runtime": "Animate", "clip": "talk_loop"},
    "rough_magic_pose": {"type": "temporary_action", "fallback": "placeholder pose until Animate rig exists"}
  }
}
```

Validation rules:

- `shot.action` must exist in the shot's scene pack or `action_registry`.
- `scene_action` must point to a valid `supported_actions` or `action_templates` entry.
- `render_action` must declare a handler and reason.
- `runtime_action` must declare a runtime and clip or state.
- `temporary_action` must declare a fallback.
- Production shots should move toward `scene_action` or `runtime_action`; `render_action` and `temporary_action` are acceptable for previews and tests.

## Required Shot Fields

Add these fields to every shot:

```yaml
event_id: breakfast_pickup
event_type: object_pickup
shot_pattern: object_pickup_sequence
camera:
  angle: eye_level | high_angle | low_angle | pov | over_shoulder | side | front | insert
  framing: wide | full | medium | closeup | extreme_closeup | insert
  lens: normal | wide | telephoto
  move: cut | push_in | pull_back | pan | tilt | truck | handheld_bump | whip
  subject: xiaoming | fridge | eggs | milk | tv | phone | friend
  motivation: establish_space | reveal_object | show_contact | show_reaction | compress_time | emphasize_joke
blocking:
  primary_action: reach | grab | pull | place | look | react | speak | enter | exit
  screen_direction: left_to_right | right_to_left | inward | outward | none
  start_anchor: fridge_handle
  end_anchor: xiaoming_hand_r
interaction:
  contact_frame: 18
  actor_anchor: xiaoming.hand_r
  prop_anchor: fridge_shelf_eggs
  result_state: prop_in_hand
edit:
  transition: action_match_cut
  continuity: hand_to_contact
  reason: cut from approach to the exact contact point
```

## Coverage Rules

For every 60 seconds:

- Use at least 14 shots unless the style intentionally imitates a stage play.
- Use at least 5 framing/angle categories across the minute.
- Use no single camera setup for more than 8 seconds.
- Use at least 4 insert or closeup shots when the story includes props, UI, food, phones, doors, screens, letters, weapons, or signs.
- Use at least 3 reaction shots. Reactions are part of the joke, not filler.
- Alternate shot sizes: wide -> medium -> closeup/insert -> reaction -> result is the default rhythm.
- Prefer cut changes over continuous decorative zoom when the story emphasis changes.

For every multi-shot event:

- Use at least two shot sizes.
- Use at least two camera angles.
- Use the required purposes for the selected `shot_pattern`.
- For phone calls and meetings, switch visible subjects instead of keeping one speaker or one master shot.
- For physical interactions, include visible result coverage after contact or pickup.
- Treat repeated `angle + framing + subject + move` longer than 8 seconds as a failed single-camera setup, even if split into multiple shot IDs.

## Pattern: Object Pickup

Use for taking food from a fridge, grabbing a phone, picking up a weapon, opening a drawer, taking documents, or stealing an item.

Minimum coverage:

```yaml
shots:
  - purpose: establish_space
    framing: wide
    angle: eye_level
    action: actor approaches object
  - purpose: contact
    framing: closeup
    angle: insert
    action: hand reaches handle or object
  - purpose: reveal_source
    framing: insert
    angle: pov
    action: show object before pickup
  - purpose: show_pickup
    framing: extreme_closeup
    angle: insert
    action: object moves from source anchor to hand anchor
  - purpose: reaction
    framing: closeup
    angle: front_or_three_quarter
    action: actor reacts or jokes
  - purpose: result
    framing: insert_or_medium
    angle: high_angle_or_eye_level
    action: object arrives at destination
```

Validation target: the prop must be visible before contact, during contact, and after the result.

## Pattern: Watch Screen / Discover Information

Use for TV, phone, monitor, magical notice, signboard, or UI popups.

Minimum coverage:

```yaml
shots:
  - purpose: establish_actor_context
    framing: medium
    action: actor is doing previous activity
  - purpose: screen_insert
    framing: insert
    angle: pov_or_front
    action: readable screen information appears
  - purpose: reaction_close
    framing: closeup
    action: actor notices and reacts
  - purpose: decision
    framing: medium
    action: actor acts on the information
```

Keep screen text large and unobstructed. Do not bury important information in a wide master shot.

## Pattern: Phone Call

Use split framing only after showing how the call begins.

Minimum coverage:

```yaml
shots:
  - purpose: pickup_phone
    framing: insert
    action: hand or prop reaches phone
  - purpose: dial_screen
    framing: insert
    action: phone UI changes to calling
  - purpose: caller_close
    framing: closeup
    action: caller speaks
  - purpose: receiver_close
    framing: closeup
    action: receiver answers
  - purpose: split_or_two_panel
    framing: medium
    action: conversation rhythm
  - purpose: decision_result
    framing: medium_or_wide
    action: meeting plan is confirmed
```

## Pattern: Meeting At Location

Use when characters meet at an event site, shop, battlefield, classroom, or gate.

Minimum coverage:

```yaml
shots:
  - purpose: location_establish
    framing: wide
    action: show geography and event signage
  - purpose: arrival
    framing: full_or_medium
    action: first character enters frame
  - purpose: counterpart_reveal
    framing: medium
    angle: over_shoulder_or_side
    action: second character appears
  - purpose: reaction_pair
    framing: closeup
    action: one character reacts
  - purpose: two_shot_result
    framing: medium_or_wide
    action: both characters share the plan
```

## Fallbacks For Missing Assets

- If no true hand rig exists, use a hand proxy closeup or object-only insert shot. Do not fake the whole interaction with a prop flying across a wide shot.
- If no alternate background angle exists, crop the wide background into motivated inserts: door handle, table top, TV, phone, fridge shelf, signboard.
- If no facial closeups exist, use silhouette closeups, reaction icons, or body-pose reaction cuts.
- If no limb articulation exists, represent contact with cut timing: before contact -> contact insert -> result state.

## Validation Checklist

Reject or revise a sequence when:

- an object interaction has no contact or insert shot;
- a prop teleports or flies without a motivated cut;
- a screen discovery stays only in a wide shot;
- the same front-facing framing carries more than 8 seconds of continuous story;
- captions cover the object or screen that the shot is about;
- a camera move exists without a `camera.motivation`;
- a shot contains more than one complex action unless it is an establishing montage.
