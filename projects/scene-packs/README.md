# Scene Packs

This folder stores reusable 2D sand-animation scene packs. Each pack should contain:

- `scene.yaml`
- `backgrounds/`
- `layers/`
- `props/`
- `previews/`

## Available Packs

### `scene_demo_school_01`

Old school exterior / corridor interaction scene.

Best for:

- phone/order popups;
- dialogue and reaction beats;
- sitting, desk interaction, reading notes;
- door/key interactions;
- blackboard and door close-up inserts.

Current coverage:

- 7 backgrounds
- 14 prop groups
- 23 anchors
- 20 supported actions

### `scene_fantasy_hall_01`

Fantasy demon-king hall scene for the delivery-to-another-world story.

Best for:

- courier entering through a portal;
- delivering a meal to a demon king;
- reading a magic order scroll;
- coin/payment handoff;
- magic warning overlays;
- throne, portal, and table staging.

Current coverage:

- 5 backgrounds
- 6 prop groups
- 13 anchors
- 10 supported actions

## Validation

Validate a pack with:

```powershell
python skills\scene-pack-builder\scripts\validate_scene_pack.py projects\scene-packs\<pack_id>
```

Preview images are part of the asset contract. If a pack changes, regenerate or update previews before committing.
