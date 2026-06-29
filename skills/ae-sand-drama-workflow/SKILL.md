---
name: ae-sand-drama-workflow
description: Build stable Chinese state-machine-driven Animate/After Effects/Remotion sand-animation short drama workflows. Use when Codex needs to create project bibles, story outlines, scene lists, shot YAML, asset manifests, AI-controlled animation state machines, Adobe Animate/Spine/Rive/Unity/AE-precomp character runtime plans, JSFL/XFL handoff specs, browser-assisted material sourcing plans, Remotion previews, After Effects editable scripts, or test animations for low-cost 2D collage/sand-animation production, especially when output format, character motion, expression/lip-sync swaps, camera movement, asset density, VFX discipline, or AE editability must be standardized.
---

# AN/AE Sand Drama Workflow

Use this skill to turn a short-drama idea into a data-driven animation production folder. AI plans story, blocking, and state timelines; an animation runtime executes approved character states; After Effects composites shots.

## Core Pipeline

1. Create a project folder under `projects/<project-id>/`.
2. Write `docs/00_Project_Bible.md`, `docs/01_Story_Outline.md`, and `docs/02_Scene_List.md` with YAML frontmatter.
3. Create `shots/<sequence>.yaml` for human review and `shots/<sequence>.json` for runtime tools.
4. Create `workflow/asset_pipeline.yaml`, `workflow/an_ae_pipeline.yaml`, and `assets/00_license_records/asset_manifest.csv`.
5. Create character state machine manifests: states, clips, allowed transitions, anchors, and runtime type.
6. Create character manifests for Animate/Spine/Rive/Unity/AE precomp runtimes: body poses, expression swaps, mouth shapes, hand/prop layers, and loopable actions.
7. Create state timelines per shot. AI outputs state changes and blocking parameters, not raw frame-by-frame animation.
8. Decompose each story beat through a cinematic shot pattern before rendering. Object interaction, screen discovery, dialogue, and meetings must become multiple short shots with motivated camera changes. Prefer generating the shot list from event beats with `scripts/expand_cinematic_beats.py`, then validating with `scripts/validate_cinematic_shots.py`.
9. Create or update runtime handoff specs. When the target runtime is unavailable, simulate the runtime layer in Remotion using the same state machine manifest.
10. Create or update a Remotion composition for quick rhythm preview.
11. Create or update an AE JSX generator that builds editable shot precomps from the same shot data and the runtime export manifest.
12. Run validation before rendering.
13. Render still checks, then render a short MP4 test.

## Agent Split

Use three roles when the user asks for multi-agent work:

- Script agent: story structure, shot beats, dialogue, jokes, character voice.
- Asset agent: material taxonomy, source search strategy, license manifest, asset intake rules.
- Runtime agent: character state machine, approved clips, transitions, anchors, and runtime export plan.
- Animate agent: Animate-specific symbol structure, expression/mouth/action loops, JSFL/XFL export plan.
- Edit agent: shot schema, motion presets, AE layer structure, validation rules, pacing.

The main agent integrates results and owns the runnable project files.

## Production Rules

- Prefer YAML/JSON data over hard-coded scene edits.
- Default to 1920x1080 horizontal 16:9 at 12 fps unless the user explicitly asks for vertical/mobile format.
- Keep AI-generated or placeholder assets clearly labeled in the license manifest.
- Keep all shot durations explicit.
- Treat the animation runtime as an executor, not a creative platform. AI selects states and timing; the runtime plays approved clips.
- Treat camera planning as an executor input, not decoration. The shot list must choose shot patterns and camera motivations before selecting transforms.
- Prefer state timelines over one-off keyframes for character acting.
- Keep character animation inside the Animate layer whenever possible: pose swaps, expression swaps, mouth loops, walk/idle/talk cycles, hand gestures, and prop holds.
- Keep AE focused on scene assembly: backgrounds, foregrounds, imported Animate sequences, camera motion, VFX, subtitles, UI, color, and final packaging.
- Do not create one giant AE timeline; make every shot a precomp and assemble a master timeline.
- Expose manual controls through predictable layer names or CTRL layers.
- Use Remotion for fast preview and validation, Animate for character motion, AE for detailed editable polishing.
- Let humans review story direction, asset choice, and pacing; scripts should catch missing fields, broken assets, invalid presets, unsafe subtitle layout, duration mismatches, missing camera blocks, asset-density gaps, and unmotivated VFX.

## Cinematic Shot Decomposition

- Before writing final shot YAML, classify each beat as `object_pickup`, `put_down`, `screen_discovery`, `phone_call`, `dialogue_exchange`, `meeting`, `travel`, `impact`, or `reaction`.
- Assign a `shot_pattern` to every beat. Use the pattern to expand one story beat into several short shots.
- Treat the expanded shot list as the production contract. The renderer should execute by `purpose`, `camera.subject`, `blocking`, and `interaction` first, then fall back to action-specific overrides only for exceptional staging.
- Do not let a single event render as one camera setup when it contains a physical interaction, screen discovery, phone call, entrance, meeting, or object transfer.
- Define a `subject_registry` in event-driven sequences. Every `camera.subject`, non-dotted blocking anchor, and non-dotted interaction prop anchor must resolve to a character, actor anchor, scene-pack background/prop/anchor, or explicit temporary fallback.
- Define an `action_registry` in event-driven sequences. Every `shot.action` must resolve to a scene-pack action template, renderer handler, runtime clip/state, or explicit temporary fallback.
- Define an `edit` block for every generated shot. It must explain `transition`, `continuity`, and `reason`, so cuts are motivated rather than arbitrary.
- Define or generate a `directing` block for every shot. It must explain `action_phase`, `focus`, `composition`, and `emphasis`, so the renderer knows what the audience should look at and why the shot exists.
- Define or generate a `continuity` block for every shot. It must explain `screen_side`, `eyeline`, `match`, and `cut_role`, so adjacent shots preserve screen direction, object-to-reaction logic, speaker reverses, and action-match cuts.
- Define or generate a `motion_plan` block for every shot. It must explain `style`, `start_scale`, `end_scale`, `start_offset`, `end_offset`, `easing`, `focus_shift`, and `parallax`, so camera movement is executable rather than decorative.
- For repeatable production, write an event file first, then run the beat expander:

```powershell
python scripts\expand_cinematic_beats.py projects\<project-id>\shots\<sequence>_events.json --output projects\<project-id>\shots\<sequence>_generated.json
python scripts\validate_cinematic_shots.py projects\<project-id>\shots\<sequence>_generated.json
```

- Do not animate a complex action in one master shot. A pickup action needs at least: establish, contact closeup, object insert, pickup/result insert, reaction.
- Validate shot rhythm per event, not only per whole video. A multi-shot event must switch at least two shot sizes and two angles; phone calls and meetings must also switch subjects.
- Require every shot pattern to include its mandatory purposes. For example, `object_pickup_sequence` must include approach/contact/source/pickup/reaction/result coverage.
- Use cuts to represent missing limb detail. If there is no hand rig, use a hand proxy, object-only insert, or before/contact/after cut. Do not make props float from one side of a wide frame to the character.
- Every shot needs `camera.angle`, `camera.framing`, `camera.move`, `camera.subject`, and `camera.motivation`.
- Every shot needs `directing.action_phase`, `directing.focus`, `directing.composition`, and `directing.emphasis`. Use these fields to separate setup, approach, contact, information, speaker, reaction, reveal, transfer, and result phases.
- Every shot needs `continuity.screen_side`, `continuity.eyeline`, `continuity.match`, and `continuity.cut_role`. The `match` value must align with `edit.continuity`.
- Every shot needs `motion_plan.style`, numeric `start_scale` / `end_scale`, two-number `start_offset` / `end_offset`, `easing`, `focus_shift`, and `parallax`. Moving cameras need visible scale or offset change and non-`none` focus shift; static cuts need no visible motion.
- Use camera moves only when the subject emphasis changes. Otherwise use a cut to a more appropriate angle.
- Write audience-facing MP4s without debug overlays, parameter labels, file names, or shot test notes.

## Renderer Execution Rules

- Build renderers as cinematic executors, not one-off storyboard drawings.
- First route a shot by `purpose`: `establish_space`, `contact`, `reveal_source`, `show_pickup`, `screen_insert`, `reaction_close`, `pickup_phone`, `dial_screen`, `caller_close`, `receiver_close`, `split_or_two_panel`, `location_establish`, `arrival`, `counterpart_reveal`, `two_shot_result`, or `result_insert`.
- Then resolve the subject through `camera.subject` and scene-pack data: background variant, foreground layer, prop variant, anchor, character state, and occlusion rule.
- Execute `motion_plan` on every shot. Map scale/offset/easing to the camera or shot precomp transform, split background and foreground movement when `parallax` is `subtle` or `layered`, and keep the caption/UI layer outside the camera transform unless the shot explicitly calls for screen-space motion.
- Use action-specific branches only when a shot needs unique layout, such as a special POV, split-screen call, large crowd reveal, or custom VFX beat.
- If the renderer cannot find an anchor or prop state, fail validation or use an explicit fallback insert. Do not silently return to a front-facing master shot.

## Edit Continuity Rules

- Treat cuts as production data. Every shot needs `edit.transition`, `edit.continuity`, and `edit.reason`.
- Use explicit transition types such as `scene_start`, `context_cut`, `insert_cut`, `action_match_cut`, `pov_cut`, `reaction_cut`, `speaker_cut`, `reverse_cut`, `result_cut`, `split_screen_bridge`, `scene_cut`, or `time_cut`.
- Scene-pack changes require `scene_cut`, `time_cut`, `graphic_match`, or `split_screen_bridge`.
- Insert/contact/result shots must use insert/action/pov/result transitions.
- Reaction and speaker shots must use reaction/speaker/reverse/result transitions.
- When returning from an insert to a character reaction, use `reaction_cut` and explain the story reason.
- Preserve pattern order. Do not shuffle contact before approach, reaction before information, or result before contact unless a deliberate flashback pattern exists and the validator has been extended for it.
- Preserve continuity roles. A contact cut should lead to a source reveal, transfer, insert, reaction, or result; a speaker cut should reverse to the receiver before bridging; an insert-to-reaction cut should declare a directional match such as `screen_to_reaction` or `object_to_reaction`.

## Subject And Anchor Binding

- Treat `camera.subject` as a bound production entity, not descriptive prose.
- Add every recurring subject to `subject_registry` with one of these types: `actor`, `actor_group`, `actor_anchor`, `scene`, `scene_anchor`, `prop`, `temporary_prop`, `temporary_anchor`, `temporary_set`, or `fallback_ui`.
- For `scene`, `scene_anchor`, and `prop`, provide `scene_pack` and the relevant `background`, `anchor`, `prop`, and optional `variant`.
- For `actor_anchor`, provide `actor` and `anchor`, such as `hand_r`.
- For temporary entries, provide a `fallback` note explaining why the subject is not yet in a scene pack.
- Run `scripts\validate_cinematic_shots.py` after expansion. It checks scene-pack existence, background keys, prop keys, anchor keys, subject registration, and temporary fallback declarations.

## Action Binding

- Treat `shot.action` as executable production data, not prose.
- Add every non-scene-pack action to `action_registry`.
- Use `scene_action` when the action maps to a scene pack's `supported_actions` or `action_templates`.
- Use `render_action` only for test/demo-specific renderer handlers, and include `handler` plus `reason`.
- Use `runtime_action` for Animate/Spine/Rive/Unity/AE-precomp clips or states, and include `runtime` plus `clip` or `state`.
- Use `temporary_action` for unresolved staging and include `fallback`.
- Prefer replacing `render_action` and `temporary_action` with `scene_action` or `runtime_action` before production rendering.
- Validation rejects unbound actions, unknown action types, missing renderer handlers, missing runtime clip/state, and missing temporary fallbacks.

## State Machine Rules

- Define each main character with a state machine manifest before generating shots.
- Required states for a production character: `idle`, `talk`, `walk`, `point`, `shock`, `recoil`. Add `attack`, `angry_talk`, `celebrate`, or `think` when the story needs them.
- Shot files must use `state_timeline` or equivalent character tracks. Each track item must include `time`, `state`, `x`, `y`, and `scale`.
- States must come from the character manifest. Unknown states are validation errors.
- Runtime outputs short reusable character clips or shot-specific transparent sequences. AE imports those outputs or a precomp proxy.
- AI may choose `state`, `timing`, `intensity`, `target`, `screen position`, and `camera focus`; AI must not invent unapproved animation poses.
- Use state-machine test clips for validation: 2-3 seconds `shock`, 3-5 seconds `talk`, 2 seconds `reaction`, and 2 seconds `attack`.

## Animate Layer Rules

- Build one Animate scene per shot or per reusable action loop, not one enormous character timeline.
- Use stable layer names: `body`, `head`, `face`, `mouth`, `left_arm`, `right_arm`, `prop`, `shadow`, `notes`.
- Use stable symbol names: `CHAR_<id>__POSE_<pose>`, `FACE_<expression>`, `MOUTH_<shape>`, `ACTION_<loop>`.
- Normalize all expression assets before animation. Every face image must share one transparent canvas size, one eye-line, and one mouth anchor. Do not place raw expression PNGs directly onto body poses.
- Define face anchors per body pose in the character manifest. Required fields: `left`, `top`, `width`, `height`, `eye_line`, and `mouth_anchor`.
- Reject a character action if the selected pose has no face anchor. Manual review should adjust the anchor table, not individual shots.
- Only replace faces on characters designed for face replacement: blank face area, stable head orientation, and approved pose anchors. For characters with painted faces or complex hair/face overlap, use full-pose expression variants or emotion bubbles instead of overlaying face PNGs.
- Export the Animate result as transparent PNG sequence by shot: `renders/an/<sequence>/<shot_id>/<character_id>/frame-0000.png`.
- If Animate is not installed, generate a Remotion preview that simulates this export layer with the same body pose, expression, mouth, gesture, and timing fields.
- Do not ask AE to perform frame-by-frame face or mouth swaps once Animate assets exist. AE should import the finished character sequence or a precomp proxy.
- Do not render internal labels such as layer names, camera preset IDs, filenames, or debug text into audience-facing MP4s. Debug overlays are allowed only in still checks or files explicitly named `debug`.

## Visual Quality Gates

- Require each shot to have a `camera` block. Use motivated camera moves such as `establishing_pan`, `push_in`, `pull_back`, `truck_left`, `over_shoulder`, `insert_closeup`, `reaction_cut`, or `static_hold`.
- Do not use one front-facing master shot for a whole sequence. In every 60 seconds, include at least 14 shots, at least 5 camera/framing/angle categories, and at least 3 distinct shot sizes: `wide`, `medium`, `closeup`, `insert`.
- No single camera setup should carry more than 8 seconds of continuous story unless the user explicitly asks for a stage-play style.
- No event should pass only because the whole sequence has enough variety. Validate every event's local shot grammar: required purposes, angle contrast, shot-size contrast, subject switching, and visible result state.
- No shot should pass with camera fields alone. Validate the shot's directing purpose: what phase it is in, what object or character gets attention, how it is composed, and what story emphasis it serves.
- No cut should pass as a naked transition label. Validate continuity fields so the renderer knows whether the cut is an establish, insert, contact, transfer, reaction, speaker, reverse, bridge, reveal, or result.
- No camera move should pass as a naked `camera.move` string. Validate `motion_plan` so push/pull/pan/truck moves have parameters, easing, focus shift, and safe crop limits.
- Reject unmotivated scene or background jumps. A shot that changes scene pack or background must explain the edit as a time cut, scene cut, insert cut, reaction cut, action match cut, or bridge.
- Every object interaction must include a visible before/contact/after structure, usually through insert shots or closeups.
- Every screen or UI discovery must include an insert shot where the information is readable and a reaction shot showing why it matters.
- Every 6-8 second shot should contain at least 2 visible action beats: pose swap, expression swap, mouth loop, gesture, prop movement, UI pop, entrance/exit, or reaction hold.
- A 60-second sequence should include at least 8 action beats and at least 2 shots with internal focus changes, such as wide-to-medium, speaker-to-reaction, or prop insert.
- Use camera movement to change emphasis, not as a constant decorative drift. Prefer deliberate multi-camera language: establishing shot, two-shot, over-shoulder, insert closeup, reaction closeup, and pull-back reveal.
- Treat VFX as story punctuation, not filler. Every non-`none` VFX must have a `vfx_reason`.
- Reject continuous random shake, unexplained flicker, and full-screen flashes that last longer than 8 frames.
- Use screen shake only for impacts, crashes, or shock beats. Limit it to 2-6 frames, amplitude <= 6 px at 1080p, and never loop it through a whole shot.
- Prefer parallax, character pose swaps, facial expression swaps, prop movement, UI animation, and camera motion over random bobbing. Idle motion should be <= 2 px and optional.
- Require asset density before rendering: every shot should have a background, at least one foreground/midground prop or UI element, visible character/subject layers, and an explicit fallback if a required asset is missing.
- If the asset library is too thin for a shot, mark the missing assets in the manifest and simplify the staging. Do not hide missing material with arbitrary smoke, flashes, or shaking.
- Reject unbound subjects. A shot cannot use `camera.subject: fridge_handle` or `interaction.prop_anchor: fridge_shelf` unless that name exists in the scene pack or `subject_registry`.
- Reject unbound actions. A shot cannot use `action: open_fridge` unless it exists in the scene pack, `action_registry`, or runtime action manifest.

## When To Use Browser/Chrome

Use Chrome or browser tooling for asset sourcing only after the asset pipeline exists. Every downloaded or candidate asset must record source URL, license, author/vendor, local path, risk level, and approval status.

## References

Read `references/shot-schema.md` when creating or revising shot YAML.
Read `references/cinematic-shot-patterns.md` when a beat contains physical action, object interaction, screen discovery, dialogue, phone calls, meetings, or any complaint about flat/single-camera staging.
Read `references/animate-layer.md` when creating character manifests, JSFL/XFL plans, or Animate export tasks.
Read `references/state-machine-runtime.md` when creating state machine manifests, runtime clips, or AI-controllable state timelines.
