---
name: sand-animation-workflow
description: Stable workflow for producing Chinese "沙雕动画"/simple cutout short dramas with Remotion preview and After Effects editable output. Use when Codex needs to create, revise, validate, or render asset-library based animation episodes, manage character pose/face calibration, build reusable motion presets, download or process free/paid materials, or generate AE-editable projects from the same story data.
---

# Sand Animation Workflow

Use this skill to produce stable asset-library animation where manual work is limited to high-level creative choices and one-time asset intake checks.

## Operating Principle

Keep production data-driven:

- Story and shot content: `project/story.json`
- Character/face anchors: `project/asset-calibration.json`
- Motion and expression rules: `project/animation-presets.json`
- Processed assets: `public/免费素材库/处理后/`
- Remotion preview: `src/Story.tsx`
- AE editable build script: `scripts/generate-ae-script.mjs`

Do not hand-tune face positions or movement curves inside a scene unless creating a new reusable preset.

## Workflow

1. Intake assets into `public/免费素材库`.
2. Run `scripts/process_free_assets.py` to create transparent, trimmed, frame-split assets under `处理后`.
3. Calibrate each character pose once in `project/asset-calibration.json`.
4. Define all allowed motion, pose, and expression changes in `project/animation-presets.json`.
5. Write or revise `project/story.json` using only calibrated `action` and `expression` values.
6. Run `scripts/validate_workflow.py` before preview or render.
7. Preview in Remotion. Fix data tables first; edit React only when the renderer lacks a reusable capability.
8. Generate AE script with `scripts/generate-ae-script.mjs`; AE should consume the same story, calibration, and motion presets.

## Quality Rules

- Prefer pose replacement, face replacement, prop movement, camera movement, and effects sprites over free-form body translation.
- Avoid long horizontal slides except for deliberate `runPast` or transition shots.
- Avoid repeated vertical bobbing for standing characters.
- Change faces at a higher frequency than body poses; body pose changes should be sparse and readable.
- Treat every new character as untrusted until all face anchors and pose dimensions are calibrated.
- If an asset is not layered by limbs, do not promise limb-level acting; use pose sheets or switch to a layered/paid/AI-generated rig.

## Validation

Run:

```powershell
python scripts/validate_workflow.py
```

Then render at least one still frame from early, middle, and effect-heavy scenes before a full render.

## References

Read `references/pipeline.md` when designing a new episode, adding asset categories, or deciding what should be automated versus manually reviewed.
