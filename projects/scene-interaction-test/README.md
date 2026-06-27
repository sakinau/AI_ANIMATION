# Scene Interaction Test

This project is a 66-second 1080p horizontal test for the scene-pack animation workflow.

## Purpose

The test checks whether existing scene packs can support basic object interaction instead of only character standing shots:

- character wakes up and moves toward a prop;
- temporary fridge opens and exposes food props;
- eggs and milk are placed on a table close-up;
- character sits, eats, and watches a TV information popup;
- character calls a friend;
- time skips to an outdoor event location;
- two characters meet at the event site.

## Source Files

- Shot plan: `projects/scene-interaction-test/shots/breakfast_activity_test.json`
- Remotion composition: `src/SceneInteractionTest.tsx`
- Test-only asset generator: `scripts/create_scene_interaction_test_assets.py`
- Render command: `scripts/render-scene-interaction-test.ps1`

## Render

```powershell
python scripts\create_scene_interaction_test_assets.py
powershell -ExecutionPolicy Bypass -File scripts\render-scene-interaction-test.ps1
```

Output:

```text
output\scene-interaction-breakfast-activity-test.mp4
```

## Cinematic Shot-Language Test

Second-pass test:

```powershell
python scripts\expand_cinematic_beats.py projects\scene-interaction-test\shots\breakfast_activity_events.json --output projects\scene-interaction-test\shots\breakfast_activity_cinematic_generated.json
python scripts\validate_cinematic_shots.py projects\scene-interaction-test\shots\breakfast_activity_cinematic_generated.json
powershell -ExecutionPolicy Bypass -File scripts\render-cinematic-interaction-test.ps1
```

Output:

```text
output\scene-interaction-breakfast-activity-cinematic-test.mp4
```

This version keeps the same rough story but expands it into 23 short shots. It tests:

- high-angle establishing shot;
- TV insert;
- reaction closeup;
- side tracking approach to fridge;
- fridge handle contact closeup;
- fridge interior POV;
- pickup closeup with a hand proxy;
- pickup result insert so the audience sees the completed state;
- table contact/result inserts;
- readable TV and notice inserts;
- phone pickup / phone screen / caller / receiver / split call coverage;
- event-site wide, over-shoulder reveal, notice insert, and two-shot result.

The important workflow change is that object interaction is no longer represented only by a prop flying in a wide shot. The action is split into before/contact/source/pickup/reaction/result coverage.

The active `CinematicInteractionTest` composition now imports:

```text
projects/scene-interaction-test/shots/breakfast_activity_cinematic_generated.json
```

That file is generated from:

```text
projects/scene-interaction-test/shots/breakfast_activity_events.json
```

The older hand-written `breakfast_activity_cinematic_test.json` remains as a reference snapshot, but the render path is now event-driven.

## Generic Purpose Renderer

`src/CinematicInteractionTest.tsx` now starts rendering each generated shot through a generic purpose layer before falling back to special action cases.

The dispatch order is:

```text
shot purpose -> camera subject -> interaction/blocking fields -> action-specific fallback
```

This keeps repeated shot types stable:

- `contact` shots render contact inserts;
- `screen_insert` and `event_notice_insert` shots render readable information inserts;
- `pickup_phone` and `dial_screen` shots render phone/table inserts;
- `reaction_close`, `caller_close`, and `receiver_close` shots render character closeups;
- `result_insert` shots render prop result inserts.

The current component still contains test-specific subject maps and temporary prop art. The next production version should resolve those from scene-pack anchors, prop states, foreground layers, and `action_templates` instead of hard-coded React branches.

## Event-Level Validation

`scripts/validate_cinematic_shots.py` now checks each event's local shot grammar, not only whole-video statistics.

It rejects:

- missing mandatory purposes for a selected shot pattern;
- physical interactions without visible result coverage;
- events with too few camera setups;
- multi-shot events without shot-size or angle contrast;
- phone calls and meetings without subject switching;
- repeated identical camera setup longer than 8 seconds, even if split into multiple shot IDs.

## Subject Registry Validation

The event source now includes a top-level `subject_registry`.

It binds subjects such as:

- `xiaoming`, `friend`, and `both` to actor entities;
- `xiaoming_hand_r` to an actor hand anchor;
- `phone`, `tv`, and `event_notice` to formal scene-pack props or anchors;
- `fridge_handle`, `eggs_milk`, and `breakfast` to explicit temporary test fallbacks.

The generated shot list carries this registry forward. `scripts/validate_cinematic_shots.py` now checks:

- every shot background exists in its `scene_pack`;
- every registered scene-pack prop, variant, background, and anchor exists in `scene.yaml`;
- every `camera.subject` is either registered or exists in the shot's scene pack;
- non-dotted blocking/interaction anchors are registered or exist in the scene pack;
- temporary subjects include a fallback note.

## Edit Continuity Validation

The generated cinematic shot list now includes an `edit` block on every shot:

```text
edit.transition
edit.continuity
edit.reason
```

This makes cuts auditable. The validator rejects:

- missing edit blocks;
- insert/contact/result shots without insert/action/pov/result transitions;
- reaction or speaker shots without reaction/speaker/reverse/result transitions;
- scene-pack jumps without `scene_cut`, `time_cut`, `graphic_match`, or `split_screen_bridge`;
- background changes inside one scene pack without an insert/context/result/reaction/POV/action-match reason.

## Action Registry Validation

The event source also includes `action_registry`.

For this test, actions are currently declared as `render_action` because they are implemented by `src/CinematicInteractionTest.tsx` rather than by formal scene-pack action templates.

`scripts/validate_cinematic_shots.py` rejects:

- `shot.action` values that are neither registered nor present in the shot's scene pack;
- unknown action registry types;
- `render_action` entries without a handler or reason;
- `scene_action` entries that do not exist in `supported_actions` / `action_templates`;
- `runtime_action` entries without a runtime and clip/state;
- `temporary_action` entries without a fallback.

The production direction is to replace preview-only `render_action` entries with scene-pack actions or Animate/AE runtime actions as rigs and templates mature.

## Asset Strategy

Formal scene packs used:

- `scene_customer_room_01`
- `scene_fantasy_market_01`
- `scene_overlay_vfx_01`

Temporary generated test assets:

- `fridge_closed.png`
- `fridge_open.png`
- `breakfast_table.png`
- `breakfast_close.png`
- `phone_call_friend.png`
- `activity_banner.png`
- `xiaoming.png`
- `friend.png`

These assets are intentionally simple and are not promoted to the formal reusable scene-pack library yet. They exist to test action choreography and object interaction first.

## Current QA Notes

- The fridge, food, table, TV, phone, and event-site interaction beats are readable.
- The event-site frame is visually crowded; later versions should add layer priority rules and automatic caption/foreground avoidance.
- Kitchen and bedroom scene packs are still missing, so the living room pack is used as a substitute.
- Hand-grip fidelity is not solved yet; object interaction is represented by staging, close-ups, and prop motion.
- The cinematic test passes `scripts/validate_cinematic_shots.py`.
- The first-pass 9-shot test intentionally fails cinematic validation, which confirms the validator catches the single-camera/master-shot problem.
