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
python scripts\validate_cinematic_shots.py projects\scene-interaction-test\shots\breakfast_activity_cinematic_test.json
powershell -ExecutionPolicy Bypass -File scripts\render-cinematic-interaction-test.ps1
```

Output:

```text
output\scene-interaction-breakfast-activity-cinematic-test.mp4
```

This version keeps the same rough story but expands it into 22 short shots. It tests:

- high-angle establishing shot;
- TV insert;
- reaction closeup;
- side tracking approach to fridge;
- fridge handle contact closeup;
- fridge interior POV;
- pickup closeup with a hand proxy;
- table contact/result inserts;
- readable TV and notice inserts;
- phone pickup / phone screen / caller / receiver / split call coverage;
- event-site wide, over-shoulder reveal, notice insert, and two-shot result.

The important workflow change is that object interaction is no longer represented only by a prop flying in a wide shot. The action is split into before/contact/source/pickup/reaction/result coverage.

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
