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
5. Expand story beats into cinematic shot patterns before writing final shots. Do not keep object interaction, phone calls, screen discoveries, or meetings in a single master shot.
6. Write or revise `project/story.json` using only calibrated `action`, `expression`, `shot_pattern`, and camera values.
7. Run `scripts/validate_workflow.py` before preview or render.
8. Preview in Remotion. Fix data tables first; edit React only when the renderer lacks a reusable capability.
9. Generate AE script with `scripts/generate-ae-script.mjs`; AE should consume the same story, calibration, and motion presets.

## Quality Rules

- Prefer pose replacement, face replacement, prop movement, camera movement, and effects sprites over free-form body translation.
- Treat cuts, inserts, and reaction shots as the primary way to make simple assets feel animated. Camera motion alone is not enough.
- For prop interaction, split the action into short shots: establish position, show contact, show object source, show pickup/result, show reaction.
- For screen information, cut to a readable screen insert and then to a reaction. Do not leave important text inside a wide shot.
- For dialogue, alternate caller/listener/reaction/two-shot instead of holding one frontal composition.
- Avoid long horizontal slides except for deliberate `runPast` or transition shots.
- Avoid repeated vertical bobbing for standing characters.
- Change faces at a higher frequency than body poses; body pose changes should be sparse and readable.
- Treat every new character as untrusted until all face anchors and pose dimensions are calibrated.
- If an asset is not layered by limbs, do not promise limb-level acting; use pose sheets or switch to a layered/paid/AI-generated rig.
- If no hand rig exists, use hand-proxy closeups or object-only insert shots. Do not represent pickup only by making the prop float to the character in a wide shot.

## Cinematic Coverage Targets

- A 60-second sample should usually contain 14-22 shots.
- Include at least 5 camera categories: wide establish, medium action, close reaction, insert/object, POV/over-shoulder/high-angle/low-angle.
- No single camera setup should last more than 8 seconds unless intentionally chosen for a stage-play gag.
- Every interaction-heavy minute should include at least 4 insert shots and 3 reaction shots.
- Audience-facing renders must not contain debug labels, parameter names, file names, or internal test notes.

## Validation

Run:

```powershell
python scripts/validate_workflow.py
```

Then render at least one still frame from early, middle, and effect-heavy scenes before a full render.

## References

Read `references/pipeline.md` when designing a new episode, adding asset categories, or deciding what should be automated versus manually reviewed.
