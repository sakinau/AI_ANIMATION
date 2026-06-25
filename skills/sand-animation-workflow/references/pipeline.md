# Stable Sand Animation Pipeline

## Asset Intake Gate

For each asset pack, classify assets before production:

- `background`: static scene images, validated by aspect ratio and readability.
- `character-pose`: full-body pose PNGs with transparent background.
- `character-rig`: layered PSD/AI/AE source with movable limbs.
- `face`: expression PNGs that can overlay a blank face.
- `effect-sprite`: GIF/PNG sequence with transparent or screen-blend background.
- `prop`: handheld or scene object.

Record source and license risk in the asset folder. Free-download pages are not automatically safe for commercial release.

## Calibration Gate

For every usable character pose, record:

- natural `width` and `height` after trimming,
- `face.centerX`, `face.centerY`, and `face.size`,
- target stage placement only once per character family.

Calibrate by rendering still frames, then freeze the values. Later episode work should not tune these numbers unless the asset itself changes.

## Motion Preset Gate

Use named motions instead of custom scene transforms:

- `still`: default speaking/listening state.
- `enter`: short entrance from nearby off-position.
- `walkIn`: small repositioning move.
- `runPast`: fast deliberate escape/chase movement.
- `hide`: vertical crouch/drop movement.

All new motion must be added to `animation-presets.json`, then reused by story actions.

## Episode Production

Generate the episode in this order:

1. Script beats and shot list.
2. Assign background, action, expression, and effect per shot.
3. Run workflow validation.
4. Render still checks.
5. Render Remotion MP4.
6. Generate AE script/project for manual editing.

Manual review should focus on story pacing, camera choices, character blocking, and whether the asset pack is expressive enough. It should not focus on recurring face offsets, missing files, unregistered actions, or renderer-specific syntax errors; those belong in validation scripts.

## When To Buy Assets

Buy or commission assets when the sample exposes one of these limits:

- full-body PNGs cannot deliver enough acting;
- pose sheets lack consistent heads or blank face areas;
- effect sprites are low resolution or legally unclear;
- backgrounds do not match story continuity.

Use AI-generated assets for prototyping and custom backgrounds. Use paid/layered packs for repeatable character acting and faster production.
