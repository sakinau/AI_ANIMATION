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
5. For physical object interactions, add `interaction.stages.before/contact/after` so the renderer knows what visible state proves each phase.
6. Expand the event file:

```powershell
python scripts\expand_cinematic_beats.py projects\<project-id>\shots\<sequence>_events.json --output projects\<project-id>\shots\<sequence>_generated.json
```

7. Validate the generated shot list:

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
3. Read `directing.action_phase`, `directing.focus`, `directing.composition`, and `directing.emphasis`.
4. Read `continuity.screen_side`, `continuity.eyeline`, `continuity.match`, and `continuity.cut_role`.
5. Read `motion_plan.style`, scale/offset endpoints, `easing`, `focus_shift`, and `parallax`.
6. Read `camera.subject`, `camera.angle`, `camera.framing`, and `camera.move`.
7. Resolve scene-pack background, foreground, prop state, and anchor data.
8. Execute the matching template for that purpose.
9. Use action-specific custom code only when the generic purpose template cannot express the shot.

Required renderer behavior:

- `contact` means show contact or near-contact in close framing.
- `screen_insert` means the screen/sign/UI information must be readable.
- `reaction_close` means the audience should see the character response, not another wide shot.
- `result_insert` means the prop or state after the action must be visible.
- `location_establish` means show geography or signage before cutting into closer shots.
- `motion_plan` means the renderer must execute the shot's scale, offset, easing, and parallax values. Do not replace these values with a renderer-local hard-coded `push_in`, `pan`, or `truck` preset.
- `interaction.stages` means the renderer must select the visible object/hand/result state for physical interaction shots. Do not treat stage names as comments.

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
- Purpose order must follow the selected shot pattern. For example, object pickup should proceed approach -> contact -> source reveal -> pickup transfer -> reaction -> result.

## Continuity Block

Every generated shot must include a `continuity` block. This is the cut-to-cut contract:

```json
{
  "continuity": {
    "screen_side": "object",
    "eyeline": "target",
    "match": "look_to_screen",
    "cut_role": "insert"
  }
}
```

Fields:

- `screen_side`: where the shot sits in screen geography, such as `actor`, `object`, `caller`, `receiver`, `pair`, `split`, or `neutral`.
- `eyeline`: how the character or insert relates visually, such as `toward_object`, `from_object`, `target`, `pov`, `to_receiver`, or `to_caller`.
- `match`: the explicit match phrase. This must equal `edit.continuity`.
- `cut_role`: the editorial role: `establish`, `context`, `action_start`, `contact`, `pov_reveal`, `insert`, `transfer`, `reaction`, `speaker`, `reverse`, `bridge`, `reveal`, or `result`.

Validation target:

- Missing `continuity` fails validation.
- `continuity.match` must match `edit.continuity`.
- `cut_role` must match the transition and shot purpose.
- Information inserts should use object/split screen side and target/POV eyeline.
- Reaction shots should return to actor screen side and preserve eyeline from the previous object or screen.
- Speaker reverse coverage should declare eyelines toward the other speaker.
- Adjacent shots must follow sensible edit grammar, such as contact -> source/transfer/reaction/result and speaker -> reverse -> bridge.

## Motion Plan

Every generated shot must include a `motion_plan` block. This is the camera-execution contract:

```json
{
  "motion_plan": {
    "style": "motivated_push",
    "start_scale": 1.0,
    "end_scale": 1.08,
    "start_offset": [0, 0],
    "end_offset": [0, -18],
    "easing": "ease_out",
    "focus_shift": "toward_subject",
    "parallax": "subtle"
  }
}
```

Fields:

- `style`: named movement family, such as `static_cut`, `motivated_push`, `reveal_pull`, `geography_pan`, or `lateral_track`.
- `start_scale` / `end_scale`: numeric crop scale. Keep values positive and normally <= `1.35`.
- `start_offset` / `end_offset`: `[x, y]` pixel offsets at 1080p.
- `easing`: `hold`, `linear_soft`, `ease_in`, `ease_out`, or `ease_in_out`.
- `focus_shift`: what the motion changes attention toward, such as `toward_subject`, `subject_to_space`, `scan_space`, or `follow_subject`.
- `parallax`: `none`, `subtle`, or `layered`.

Validation target:

- Missing `motion_plan` fails validation.
- Moving cameras (`push_in`, `pull_back`, `pan`, `truck`) need visible scale or offset change.
- Static cuts should not include visible motion.
- Moving cameras need non-`none` `focus_shift`.
- Lateral moves need `subtle` or `layered` parallax.
- Motion style should match `camera.move`.
- Scale values above `1.35` fail to avoid over-cropping 2D collage assets.
- The whole sequence needs enough visible camera motion for its runtime.
- Every event with three or more shots needs at least one visible camera move.
- Events with four or more shots should include at least two non-static motion styles.

Renderer target:

- Apply `start_scale` -> `end_scale` and `start_offset` -> `end_offset` over the shot duration with the declared `easing`.
- Keep audience subtitles and debug-free UI outside the camera transform unless they are part of an in-world screen.
- For `parallax: subtle`, move background layers at a reduced factor and foreground/character layers at full factor.
- For `parallax: layered`, move background, midground, foreground, and character layers at separate factors when those layers exist; use at least background-vs-foreground separation in Remotion previews.
- Add safe crop compensation during execution so offset motion does not reveal black frame edges.
- Dialogue and phone-call patterns should use small motivated moves, such as push-in on a readable insert or speaker close-up and pull-back on a shared decision, rather than leaving every reverse shot static.

## Directing Block

Every generated shot must include a `directing` block. This is the director-facing contract that prevents the renderer from treating all shots as interchangeable camera transforms:

```json
{
  "directing": {
    "action_phase": "contact",
    "focus": "hand_or_object_contact",
    "composition": "contact_point_priority",
    "emphasis": "sell the physical touch or placement"
  }
}
```

Use `action_phase` to describe where the shot sits inside the beat:

- `setup`: establish space or previous activity.
- `approach`: actor moves toward the object or target.
- `contact`: physical touch, button press, pickup start, or placement moment.
- `source_reveal`: show what is inside, behind, or about to be taken.
- `transfer`: object moves from source to hand or hand to destination.
- `information`: readable screen, notice, phone UI, sign, or popup.
- `speaker` / `reverse_speaker`: dialogue performance and reverse cut.
- `reaction` / `shared_reaction`: character response after information or action.
- `reveal`: introduce a counterpart, location detail, or hidden subject.
- `result` / `shared_result`: confirm the new object, location, or decision state.

Validation target:

- Missing `directing` fails validation.
- `action_phase` must match the shot purpose.
- Information inserts must have readable screen/sign/notice focus.
- Physical action inserts must name hand/object/contact/transfer focus.
- Reaction shots must name reaction focus.
- Result shots must name result focus.

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
- Physical interactions must include `interaction.actor_anchor`, `interaction.prop_anchor`, `interaction.contact_frame`, `interaction.result_state`, and `interaction.stages.before/contact/after`.
- Each interaction stage must declare `purpose`, `anchor`, and `visible_state`; the purpose must exist in that event's expanded shots.
- Stage anchors can resolve to scene anchors, scene props, or subject_registry entries.
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
directing:
  action_phase: contact
  focus: hand_or_object_contact
  composition: contact_point_priority
  emphasis: sell the physical touch before the result
continuity:
  screen_side: object
  eyeline: none
  match: hand_to_contact
  cut_role: contact
motion_plan:
  style: static_cut
  start_scale: 1.0
  end_scale: 1.0
  start_offset: [0, 0]
  end_offset: [0, 0]
  easing: hold
  focus_shift: none
  parallax: none
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
  stages:
    before: {purpose: reveal_source, anchor: fridge_shelf_eggs, visible_state: eggs_on_shelf}
    contact: {purpose: show_pickup, anchor: xiaoming_hand_r, visible_state: hand_closes_on_food}
    after: {purpose: result_insert, anchor: xiaoming_hand_r, visible_state: food_in_hand}
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
- The renderer should read the stage matching the current shot purpose and use `visible_state` to choose prop position, hand proxy position, opacity, rotation, or the result insert variant.

## Validation Checklist

Reject or revise a sequence when:

- an object interaction has no contact or insert shot;
- a prop teleports or flies without a motivated cut;
- a screen discovery stays only in a wide shot;
- the same front-facing framing carries more than 8 seconds of continuous story;
- captions cover the object or screen that the shot is about;
- a camera move exists without a `camera.motivation`;
- a shot contains more than one complex action unless it is an establishing montage.
