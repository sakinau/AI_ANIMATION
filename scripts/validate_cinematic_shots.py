import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


INTERACTION_TYPES = {
    "object_pickup",
    "put_down",
    "screen_discovery",
    "phone_call",
    "meeting",
}

INTERACTION_ACTION_HINTS = (
    "pick",
    "pickup",
    "take",
    "grab",
    "open_fridge",
    "call",
    "phone",
    "watch",
    "screen",
    "tv",
    "meet",
)

PATTERN_REQUIRED_PURPOSES = {
    "establish_to_reaction": {"establish_space", "screen_insert", "reaction_close"},
    "object_pickup_sequence": {"approach_object", "contact", "reveal_source", "show_pickup", "reaction", "result_insert"},
    "object_putdown_sequence": {"contact", "result_insert"},
    "watch_screen_discovery": {"actor_context", "screen_insert", "reaction_close"},
    "phone_call": {"pickup_phone", "dial_screen", "caller_close", "receiver_close", "split_result"},
    "meeting_at_location": {"location_establish", "counterpart_reveal", "event_notice_insert", "reaction_pair_result"},
}

MIN_EVENT_CAMERA_SETUPS = {
    "establish_to_reaction": 3,
    "object_pickup_sequence": 5,
    "object_putdown_sequence": 2,
    "watch_screen_discovery": 3,
    "phone_call": 4,
    "meeting_at_location": 4,
}

TEMPORARY_SUBJECT_TYPES = {"temporary_prop", "temporary_anchor", "temporary_set", "fallback_ui"}
ACTOR_SUBJECT_TYPES = {"actor", "actor_group", "actor_anchor"}
ANCHOR_REGISTRY_TYPES = TEMPORARY_SUBJECT_TYPES | {"actor_anchor"}
ACTION_REGISTRY_TYPES = {"scene_action", "render_action", "temporary_action", "runtime_action"}
SCENE_CHANGE_TRANSITIONS = {"scene_cut", "time_cut", "graphic_match", "split_screen_bridge"}
INSERT_PURPOSES = {"screen_insert", "event_notice_insert", "dial_screen", "pickup_phone", "contact", "reveal_source", "show_pickup", "result_insert"}
REACTION_PURPOSES = {"reaction", "reaction_close", "caller_close", "receiver_close", "reaction_pair_result"}


def load_sequence(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def find_scene_packs_root(shot_json: Path) -> Path:
    candidates = [
        Path.cwd() / "projects" / "scene-packs",
        shot_json.resolve().parents[2] / "scene-packs" if len(shot_json.resolve().parents) > 2 else Path(""),
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return Path.cwd() / "projects" / "scene-packs"


def load_scene_pack(scene_packs_root: Path, scene_pack_id: str, cache: dict[str, dict | None]) -> dict | None:
    if not scene_pack_id:
        return None
    if scene_pack_id in cache:
        return cache[scene_pack_id]
    scene_yaml = scene_packs_root / scene_pack_id / "scene.yaml"
    if not scene_yaml.exists():
        cache[scene_pack_id] = None
        return None
    with scene_yaml.open("r", encoding="utf-8-sig") as fh:
        data = yaml.safe_load(fh) or {}
    cache[scene_pack_id] = data
    return data


def camera_field(shot: dict, key: str) -> str:
    camera = shot.get("camera", {})
    if isinstance(camera, str):
        return camera if key in {"preset", "move"} else ""
    if isinstance(camera, dict):
        return str(camera.get(key, "") or "")
    return ""


def shot_event_type(shot: dict) -> str:
    event_type = str(shot.get("event_type", "") or "")
    if event_type:
        return event_type
    action = str(shot.get("action", "") or "").lower()
    if any(hint in action for hint in INTERACTION_ACTION_HINTS):
        return "interaction"
    return ""


def camera_signature(shot: dict) -> tuple[str, str, str]:
    return (
        camera_field(shot, "angle"),
        camera_field(shot, "framing"),
        camera_field(shot, "subject") or str(shot.get("subject", "") or ""),
    )


def camera_setup(shot: dict) -> tuple[str, str, str, str]:
    return (
        camera_field(shot, "angle"),
        camera_field(shot, "framing"),
        camera_field(shot, "subject") or str(shot.get("subject", "") or ""),
        camera_field(shot, "move") or camera_field(shot, "preset"),
    )


def edit_field(shot: dict, key: str) -> str:
    edit = shot.get("edit", {})
    if isinstance(edit, dict):
        return str(edit.get(key, "") or "")
    return ""


def registry_subject_errors(subject: str, binding: dict, scene_packs_root: Path, scene_cache: dict[str, dict | None]) -> list[str]:
    errors: list[str] = []
    subject_type = str(binding.get("type", "") or "")
    if not subject_type:
        errors.append(f"subject_registry.{subject}: missing type.")
        return errors
    if subject_type in ACTOR_SUBJECT_TYPES or subject_type in TEMPORARY_SUBJECT_TYPES:
        if subject_type in TEMPORARY_SUBJECT_TYPES and not binding.get("fallback"):
            errors.append(f"subject_registry.{subject}: temporary subject must declare fallback.")
        return errors

    scene_pack_id = str(binding.get("scene_pack", "") or "")
    if not scene_pack_id:
        errors.append(f"subject_registry.{subject}: {subject_type} subject must declare scene_pack.")
        return errors
    scene = load_scene_pack(scene_packs_root, scene_pack_id, scene_cache)
    if scene is None:
        errors.append(f"subject_registry.{subject}: scene_pack not found: {scene_pack_id}.")
        return errors

    background = binding.get("background")
    if background and background not in (scene.get("backgrounds") or {}):
        errors.append(f"subject_registry.{subject}: background {background} not found in {scene_pack_id}.")

    anchor = binding.get("anchor")
    if anchor and anchor not in (scene.get("anchors") or {}):
        errors.append(f"subject_registry.{subject}: anchor {anchor} not found in {scene_pack_id}.")

    prop = binding.get("prop")
    if prop:
        props = scene.get("props") or {}
        if prop not in props:
            errors.append(f"subject_registry.{subject}: prop {prop} not found in {scene_pack_id}.")
        else:
            variant = binding.get("variant")
            variants = (props.get(prop) or {}).get("variants") or {}
            if variant and variant not in variants:
                errors.append(f"subject_registry.{subject}: variant {variant} for prop {prop} not found in {scene_pack_id}.")
    return errors


def shot_subject_errors(shot: dict, registry: dict, scene_packs_root: Path, scene_cache: dict[str, dict | None]) -> list[str]:
    shot_id = shot.get("shot_id", "<unknown>")
    subject = camera_field(shot, "subject")
    scene_pack_id = str(shot.get("scene_pack", "") or "")
    errors: list[str] = []
    if not subject:
        return errors
    if subject in registry:
        return errors

    scene = load_scene_pack(scene_packs_root, scene_pack_id, scene_cache)
    if scene is None:
        errors.append(f"{shot_id}: scene_pack not found: {scene_pack_id}.")
        return errors

    known = set(scene.get("anchors") or {}) | set(scene.get("props") or {}) | set(scene.get("backgrounds") or {})
    if subject not in known:
        errors.append(f"{shot_id}: camera.subject '{subject}' is not in subject_registry or scene_pack {scene_pack_id}.")
    return errors


def interaction_anchor_errors(shot: dict, registry: dict, scene_packs_root: Path, scene_cache: dict[str, dict | None]) -> list[str]:
    shot_id = shot.get("shot_id", "<unknown>")
    scene_pack_id = str(shot.get("scene_pack", "") or "")
    scene = load_scene_pack(scene_packs_root, scene_pack_id, scene_cache)
    scene_anchors = set((scene or {}).get("anchors") or {})
    errors: list[str] = []

    def check_anchor(anchor: str, label: str) -> None:
        if not anchor or "." in anchor:
            return
        if anchor in scene_anchors:
            return
        binding = registry.get(anchor)
        if binding and str(binding.get("type", "") or "") in ANCHOR_REGISTRY_TYPES:
            return
        errors.append(f"{shot_id}: {label} anchor '{anchor}' is not in scene_pack {scene_pack_id} or temporary subject_registry.")

    blocking = shot.get("blocking") or {}
    interaction = shot.get("interaction") or {}
    if isinstance(blocking, dict):
        check_anchor(str(blocking.get("start_anchor", "") or ""), "blocking.start_anchor")
        check_anchor(str(blocking.get("end_anchor", "") or ""), "blocking.end_anchor")
    if isinstance(interaction, dict):
        check_anchor(str(interaction.get("prop_anchor", "") or ""), "interaction.prop_anchor")
    return errors


def action_errors(shot: dict, action_registry: dict, scene_packs_root: Path, scene_cache: dict[str, dict | None]) -> list[str]:
    shot_id = shot.get("shot_id", "<unknown>")
    action = str(shot.get("action", "") or "")
    if not action:
        return [f"{shot_id}: missing action."]

    scene_pack_id = str(shot.get("scene_pack", "") or "")
    scene = load_scene_pack(scene_packs_root, scene_pack_id, scene_cache)
    scene_actions = set()
    if scene:
        scene_actions |= set(scene.get("supported_actions") or [])
        scene_actions |= set((scene.get("action_templates") or {}).keys())
    if action in scene_actions and action not in action_registry:
        return []

    binding = action_registry.get(action)
    if not binding:
        return [f"{shot_id}: action '{action}' is not in action_registry or scene_pack {scene_pack_id} actions."]
    if not isinstance(binding, dict):
        return [f"action_registry.{action}: binding must be an object."]

    action_type = str(binding.get("type", "") or "")
    errors: list[str] = []
    if action_type not in ACTION_REGISTRY_TYPES:
        errors.append(f"action_registry.{action}: unknown type '{action_type}'.")
        return errors

    if action_type == "scene_action":
        bound_scene_pack = str(binding.get("scene_pack", "") or scene_pack_id)
        bound_action = str(binding.get("action", "") or action)
        bound_scene = load_scene_pack(scene_packs_root, bound_scene_pack, scene_cache)
        if bound_scene is None:
            errors.append(f"action_registry.{action}: scene_pack not found: {bound_scene_pack}.")
        else:
            allowed = set(bound_scene.get("supported_actions") or []) | set((bound_scene.get("action_templates") or {}).keys())
            if bound_action not in allowed:
                errors.append(f"action_registry.{action}: scene action '{bound_action}' not found in {bound_scene_pack}.")
    elif action_type == "render_action":
        if not binding.get("handler"):
            errors.append(f"action_registry.{action}: render_action must declare handler.")
        if not binding.get("reason"):
            errors.append(f"action_registry.{action}: render_action must declare reason.")
    elif action_type == "runtime_action":
        if not binding.get("runtime"):
            errors.append(f"action_registry.{action}: runtime_action must declare runtime.")
        if not binding.get("clip") and not binding.get("state"):
            errors.append(f"action_registry.{action}: runtime_action must declare clip or state.")
    elif action_type == "temporary_action":
        if not binding.get("fallback"):
            errors.append(f"action_registry.{action}: temporary_action must declare fallback.")
    return errors


def edit_errors(shots: list[dict]) -> list[str]:
    errors: list[str] = []
    for index, shot in enumerate(shots):
        shot_id = shot.get("shot_id", "<unknown>")
        edit = shot.get("edit")
        if not isinstance(edit, dict):
            errors.append(f"{shot_id}: missing edit block with transition/continuity/reason.")
            continue
        for key in ("transition", "continuity", "reason"):
            if not edit.get(key):
                errors.append(f"{shot_id}: missing edit.{key}.")

        purpose = str(shot.get("purpose", "") or "")
        transition = edit_field(shot, "transition")
        if purpose in INSERT_PURPOSES and transition not in {"insert_cut", "action_match_cut", "pov_cut", "result_cut"}:
            errors.append(f"{shot_id}: insert/contact purpose '{purpose}' needs insert/action/pov/result edit transition, got '{transition}'.")
        if purpose in REACTION_PURPOSES and transition not in {"reaction_cut", "speaker_cut", "reverse_cut", "result_cut"}:
            errors.append(f"{shot_id}: reaction/speaker purpose '{purpose}' needs reaction/speaker/reverse/result edit transition, got '{transition}'.")

        if index == 0:
            if transition not in {"scene_start", "context_cut", "time_cut"}:
                errors.append(f"{shot_id}: first shot should start with scene_start/context_cut/time_cut, got '{transition}'.")
            continue

        previous = shots[index - 1]
        previous_scene = str(previous.get("scene_pack", "") or "")
        current_scene = str(shot.get("scene_pack", "") or "")
        previous_event = str(previous.get("event_id", "") or "")
        current_event = str(shot.get("event_id", "") or "")
        previous_background = str(previous.get("background", "") or "")
        current_background = str(shot.get("background", "") or "")

        if previous_scene != current_scene and transition not in SCENE_CHANGE_TRANSITIONS:
            errors.append(f"{shot_id}: scene_pack changes from {previous_scene} to {current_scene} but edit.transition is '{transition}'.")
        if previous_event != current_event and previous_scene != current_scene and transition not in SCENE_CHANGE_TRANSITIONS:
            errors.append(f"{shot_id}: new event changes scene without scene/time/bridge transition.")
        if previous_background != current_background and previous_scene == current_scene:
            if transition not in {"insert_cut", "pov_cut", "action_match_cut", "context_cut", "result_cut", "reaction_cut", "scene_start", "time_cut"}:
                errors.append(f"{shot_id}: background changes within {current_scene} without insert/context/result edit transition.")
    return errors


def validate(path: Path) -> list[str]:
    data = load_sequence(path)
    shots = data.get("shots", [])
    errors: list[str] = []
    warnings: list[str] = []
    registry = data.get("subject_registry", {})
    if not isinstance(registry, dict):
        registry = {}
        errors.append("subject_registry must be an object when present.")
    action_registry = data.get("action_registry", {})
    if not isinstance(action_registry, dict):
        action_registry = {}
        errors.append("action_registry must be an object when present.")
    scene_packs_root = find_scene_packs_root(path)
    scene_cache: dict[str, dict | None] = {}

    if not shots:
        return ["No shots found."]

    errors.extend(edit_errors(shots))

    runtime = float(data.get("runtime_seconds") or sum(float(s.get("duration", 0)) for s in shots))
    expected_min = max(1, round(runtime / 60 * 14))
    if len(shots) < expected_min:
        errors.append(f"Shot count too low: {len(shots)} shots for {runtime:g}s, expected at least {expected_min}.")

    total_duration = sum(float(s.get("duration", 0)) for s in shots)
    if runtime and abs(total_duration - runtime) > 0.2:
        warnings.append(f"Shot durations sum to {total_duration:g}s but runtime_seconds is {runtime:g}s.")

    framing = Counter(camera_field(s, "framing") or str(s.get("framing", "") or "") for s in shots)
    angle = Counter(camera_field(s, "angle") for s in shots)
    move = Counter(camera_field(s, "move") or camera_field(s, "preset") for s in shots)
    subjects = Counter(camera_field(s, "subject") or str(s.get("subject", "") or "") for s in shots)

    framing.pop("", None)
    angle.pop("", None)
    move.pop("", None)
    subjects.pop("", None)

    categories = set(framing) | {f"angle:{name}" for name in angle} | {f"move:{name}" for name in move}
    if len(categories) < 5:
        errors.append(f"Camera variety too low: {len(categories)} categories found, expected at least 5.")

    insert_like = sum(
        1
        for s in shots
        if (camera_field(s, "framing") or s.get("framing")) in {"insert", "closeup", "extreme_closeup"}
        or camera_field(s, "angle") in {"insert", "pov", "over_shoulder", "high_angle", "low_angle"}
    )
    min_insert = max(2, round(runtime / 60 * 4))
    if insert_like < min_insert:
        errors.append(f"Insert/close coverage too low: {insert_like}, expected at least {min_insert}.")

    reaction_count = sum(
        1
        for s in shots
        if "reaction" in str(s.get("purpose", "")).lower()
        or "react" in str(s.get("action", "")).lower()
        or camera_field(s, "motivation") == "show_reaction"
    )
    min_reaction = max(1, round(runtime / 60 * 3))
    if reaction_count < min_reaction:
        errors.append(f"Reaction coverage too low: {reaction_count}, expected at least {min_reaction}.")

    for shot in shots:
        shot_id = shot.get("shot_id", "<unknown>")
        duration = float(shot.get("duration", 0) or 0)
        scene_pack_id = str(shot.get("scene_pack", "") or "")
        scene = load_scene_pack(scene_packs_root, scene_pack_id, scene_cache)
        if scene is None:
            errors.append(f"{shot_id}: scene_pack not found: {scene_pack_id}.")
        else:
            background = str(shot.get("background", "") or "")
            if background and background not in (scene.get("backgrounds") or {}):
                errors.append(f"{shot_id}: background '{background}' not found in scene_pack {scene_pack_id}.")
        if duration > 8:
            errors.append(f"{shot_id}: duration {duration:g}s exceeds 8s single-camera limit.")
        camera = shot.get("camera")
        if not isinstance(camera, dict):
            errors.append(f"{shot_id}: camera must be an object with angle/framing/move/subject/motivation.")
            continue
        for key in ("angle", "framing", "move", "subject", "motivation"):
            if not camera.get(key):
                errors.append(f"{shot_id}: missing camera.{key}.")
        if not shot.get("shot_pattern"):
            errors.append(f"{shot_id}: missing shot_pattern.")
        errors.extend(shot_subject_errors(shot, registry, scene_packs_root, scene_cache))
        errors.extend(interaction_anchor_errors(shot, registry, scene_packs_root, scene_cache))
        errors.extend(action_errors(shot, action_registry, scene_packs_root, scene_cache))

    used_subjects = {camera_field(shot, "subject") for shot in shots if camera_field(shot, "subject")}
    for subject in sorted(used_subjects & set(registry)):
        binding = registry.get(subject) or {}
        if isinstance(binding, dict):
            errors.extend(registry_subject_errors(subject, binding, scene_packs_root, scene_cache))
        else:
            errors.append(f"subject_registry.{subject}: binding must be an object.")

    by_event: dict[str, list[dict]] = defaultdict(list)
    for shot in shots:
        event_id = str(shot.get("event_id", "") or shot.get("shot_id", ""))
        by_event[event_id].append(shot)

    for event_id, event_shots in by_event.items():
        event_types = {shot_event_type(s) for s in event_shots}
        shot_pattern = str(event_shots[0].get("shot_pattern", "") or "")
        purposes = {str(s.get("purpose", "") or "") for s in event_shots}
        required_purposes = PATTERN_REQUIRED_PURPOSES.get(shot_pattern)
        if required_purposes:
            missing = sorted(required_purposes - purposes)
            if missing:
                errors.append(f"{event_id}: {shot_pattern} missing required purposes: {', '.join(missing)}.")

        if len(event_shots) >= 3:
            signatures = {camera_signature(s) for s in event_shots}
            framings = {camera_field(s, "framing") for s in event_shots}
            angles = {camera_field(s, "angle") for s in event_shots}
            subjects_in_event = {camera_field(s, "subject") for s in event_shots}
            framings.discard("")
            angles.discard("")
            subjects_in_event.discard("")
            min_setups = min(len(event_shots), MIN_EVENT_CAMERA_SETUPS.get(shot_pattern, 3))
            if len(signatures) < min_setups:
                errors.append(f"{event_id}: camera setups too repetitive for {shot_pattern}: {len(signatures)} found, expected at least {min_setups}.")
            if len(framings) < 2:
                errors.append(f"{event_id}: event lacks shot-size contrast; expected at least 2 framings.")
            if len(angles) < 2:
                errors.append(f"{event_id}: event lacks angle contrast; expected at least 2 angles.")
            if shot_pattern in {"phone_call", "meeting_at_location"} and len(subjects_in_event) < 2:
                errors.append(f"{event_id}: multi-character event lacks subject switching.")

        if not (event_types & INTERACTION_TYPES or "interaction" in event_types):
            continue
        purpose_text = " ".join(str(s.get("purpose", "") or "").lower() for s in event_shots)
        framings = {camera_field(s, "framing") for s in event_shots}
        motivations = {camera_field(s, "motivation") for s in event_shots}
        has_insert = bool(framings & {"insert", "closeup", "extreme_closeup"})
        has_contact = "contact" in purpose_text or "show_contact" in motivations
        has_reaction = "reaction" in purpose_text or "show_reaction" in motivations
        has_result = "result" in purpose_text or "show_result" in motivations
        if len(event_shots) < 2:
            errors.append(f"{event_id}: interaction event has only one shot.")
        if not has_insert:
            errors.append(f"{event_id}: interaction event lacks insert/closeup coverage.")
        if ("object_pickup" in event_types or "interaction" in event_types) and not has_contact:
            errors.append(f"{event_id}: pickup/contact event lacks contact coverage.")
        if ("object_pickup" in event_types or "put_down" in event_types or "interaction" in event_types) and not has_result:
            errors.append(f"{event_id}: object interaction lacks visible result coverage.")
        if ("screen_discovery" in event_types or "phone_call" in event_types) and not has_reaction:
            errors.append(f"{event_id}: discovery/call event lacks reaction coverage.")

    current_setup = None
    setup_duration = 0.0
    setup_start = ""
    for shot in shots:
        setup = camera_setup(shot)
        duration = float(shot.get("duration", 0) or 0)
        if setup == current_setup:
            setup_duration += duration
        else:
            if current_setup and setup_duration > 8:
                errors.append(f"{setup_start}: repeated camera setup runs {setup_duration:g}s, exceeding 8s continuous setup limit.")
            current_setup = setup
            setup_duration = duration
            setup_start = str(shot.get("shot_id", "<unknown>"))
    if current_setup and setup_duration > 8:
        errors.append(f"{setup_start}: repeated camera setup runs {setup_duration:g}s, exceeding 8s continuous setup limit.")

    return errors + [f"WARNING: {warning}" for warning in warnings]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cinematic shot coverage for sand-animation JSON shot lists.")
    parser.add_argument("shot_json", type=Path)
    args = parser.parse_args()

    issues = validate(args.shot_json)
    if issues:
        print("Cinematic shot validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"OK: cinematic shot coverage looks usable for {args.shot_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
