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
