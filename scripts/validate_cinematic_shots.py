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

PATTERN_PURPOSE_ORDER = {
    "establish_to_reaction": ["establish_space", "screen_insert", "reaction_close"],
    "object_pickup_sequence": ["approach_object", "contact", "reveal_source", "show_pickup", "reaction", "result_insert"],
    "object_putdown_sequence": ["contact", "result_insert"],
    "watch_screen_discovery": ["actor_context", "screen_insert", "reaction_close"],
    "phone_call": ["pickup_phone", "dial_screen", "caller_close", "receiver_close", "split_result"],
    "meeting_at_location": ["location_establish", "counterpart_reveal", "event_notice_insert", "reaction_pair_result"],
}

PURPOSE_ACTION_PHASES = {
    "establish_space": {"setup"},
    "screen_insert": {"information"},
    "reaction_close": {"reaction"},
    "approach_object": {"approach"},
    "contact": {"contact"},
    "reveal_source": {"source_reveal", "information"},
    "show_pickup": {"transfer"},
    "reaction": {"reaction"},
    "result_insert": {"result"},
    "actor_context": {"setup"},
    "pickup_phone": {"contact"},
    "dial_screen": {"information"},
    "caller_close": {"speaker"},
    "receiver_close": {"reverse_speaker", "speaker"},
    "split_result": {"shared_result"},
    "location_establish": {"setup"},
    "counterpart_reveal": {"reveal"},
    "event_notice_insert": {"information"},
    "reaction_pair_result": {"shared_reaction", "reaction"},
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
DIRECTING_REQUIRED_FIELDS = {"action_phase", "focus", "composition", "emphasis"}
CONTINUITY_REQUIRED_FIELDS = {"screen_side", "eyeline", "match", "cut_role"}
MOTION_REQUIRED_FIELDS = {"style", "start_scale", "end_scale", "start_offset", "end_offset", "easing", "focus_shift", "parallax"}
MOTION_MOVES = {"push_in", "pull_back", "pan", "tilt", "truck", "handheld_bump", "whip"}
STATIC_MOVES = {"cut", "static_hold"}
MOVE_STYLE_PREFIX = {
    "cut": {"static", "hold"},
    "push_in": {"motivated", "push"},
    "pull_back": {"reveal", "pull"},
    "pan": {"geography", "pan", "scan"},
    "truck": {"lateral", "track", "truck"},
}
TRANSITION_CUT_ROLES = {
    "scene_start": {"establish"},
    "context_cut": {"context", "establish"},
    "insert_cut": {"insert"},
    "action_start": {"action_start"},
    "action_match_cut": {"contact", "transfer"},
    "pov_cut": {"pov_reveal", "insert"},
    "reaction_cut": {"reaction"},
    "speaker_cut": {"speaker"},
    "reverse_cut": {"reverse"},
    "result_cut": {"result"},
    "split_screen_bridge": {"bridge"},
    "scene_cut": {"establish"},
    "time_cut": {"establish"},
    "graphic_match": {"bridge", "insert", "result"},
}
PURPOSE_CUT_ROLES = {
    "establish_space": {"establish"},
    "screen_insert": {"insert"},
    "reaction_close": {"reaction"},
    "approach_object": {"action_start"},
    "contact": {"contact"},
    "reveal_source": {"pov_reveal", "insert"},
    "show_pickup": {"transfer"},
    "reaction": {"reaction"},
    "result_insert": {"result"},
    "actor_context": {"context"},
    "pickup_phone": {"contact"},
    "dial_screen": {"insert"},
    "caller_close": {"speaker"},
    "receiver_close": {"reverse"},
    "split_result": {"bridge"},
    "location_establish": {"establish"},
    "counterpart_reveal": {"reveal"},
    "event_notice_insert": {"insert"},
    "reaction_pair_result": {"result"},
}


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


def directing_errors(shot: dict) -> list[str]:
    shot_id = shot.get("shot_id", "<unknown>")
    directing = shot.get("directing")
    if not isinstance(directing, dict):
        return [f"{shot_id}: missing directing block with action_phase/focus/composition/emphasis."]

    errors: list[str] = []
    for key in sorted(DIRECTING_REQUIRED_FIELDS):
        if not directing.get(key):
            errors.append(f"{shot_id}: missing directing.{key}.")

    purpose = str(shot.get("purpose", "") or "")
    action_phase = str(directing.get("action_phase", "") or "")
    allowed = PURPOSE_ACTION_PHASES.get(purpose)
    if allowed and action_phase and action_phase not in allowed:
        errors.append(f"{shot_id}: purpose '{purpose}' expects directing.action_phase in {sorted(allowed)}, got '{action_phase}'.")

    framing = camera_field(shot, "framing")
    composition = str(directing.get("composition", "") or "")
    focus = str(directing.get("focus", "") or "")
    if purpose in INSERT_PURPOSES and framing not in {"insert", "closeup", "extreme_closeup"}:
        errors.append(f"{shot_id}: insert/contact purpose '{purpose}' should use close or insert framing, got '{framing}'.")
    if purpose in {"screen_insert", "dial_screen", "event_notice_insert"}:
        readable_terms = ("readable", "screen", "notice", "sign")
        if not any(term in focus or term in composition for term in readable_terms):
            errors.append(f"{shot_id}: information insert needs readable screen/sign focus in directing.")
    if purpose in {"contact", "pickup_phone", "show_pickup"}:
        contact_terms = ("contact", "hand", "object", "phone", "transfer")
        if not any(term in focus or term in composition for term in contact_terms):
            errors.append(f"{shot_id}: physical action insert needs hand/object/contact focus in directing.")
    if purpose in {"reaction", "reaction_close", "reaction_pair_result"} and "reaction" not in focus and "reaction" not in action_phase:
        errors.append(f"{shot_id}: reaction purpose needs reaction focus in directing.")
    if purpose in {"caller_close", "receiver_close"} and "performance" not in focus and "speaker" not in action_phase:
        errors.append(f"{shot_id}: speaker closeup needs performance or speaker focus in directing.")
    if purpose in {"result_insert", "split_result", "reaction_pair_result"} and "result" not in focus and "result" not in action_phase:
        errors.append(f"{shot_id}: result purpose needs result focus in directing.")
    return errors


def continuity_errors(shot: dict) -> list[str]:
    shot_id = shot.get("shot_id", "<unknown>")
    continuity = shot.get("continuity")
    if not isinstance(continuity, dict):
        return [f"{shot_id}: missing continuity block with screen_side/eyeline/match/cut_role."]

    errors: list[str] = []
    for key in sorted(CONTINUITY_REQUIRED_FIELDS):
        if not continuity.get(key):
            errors.append(f"{shot_id}: missing continuity.{key}.")

    match = str(continuity.get("match", "") or "")
    cut_role = str(continuity.get("cut_role", "") or "")
    edit_continuity = edit_field(shot, "continuity")
    transition = edit_field(shot, "transition")
    purpose = str(shot.get("purpose", "") or "")

    if edit_continuity and match and edit_continuity != match:
        errors.append(f"{shot_id}: continuity.match '{match}' must match edit.continuity '{edit_continuity}'.")

    allowed_roles = TRANSITION_CUT_ROLES.get(transition)
    if allowed_roles and cut_role and cut_role not in allowed_roles:
        errors.append(f"{shot_id}: edit.transition '{transition}' expects continuity.cut_role in {sorted(allowed_roles)}, got '{cut_role}'.")

    purpose_roles = PURPOSE_CUT_ROLES.get(purpose)
    if purpose_roles and cut_role and cut_role not in purpose_roles:
        errors.append(f"{shot_id}: purpose '{purpose}' expects continuity.cut_role in {sorted(purpose_roles)}, got '{cut_role}'.")

    if purpose in {"screen_insert", "dial_screen", "event_notice_insert"}:
        if str(continuity.get("screen_side", "") or "") not in {"object", "split"}:
            errors.append(f"{shot_id}: information insert should put continuity.screen_side on object or split.")
        if str(continuity.get("eyeline", "") or "") not in {"target", "pov"}:
            errors.append(f"{shot_id}: information insert should use target or pov eyeline.")
    if purpose in {"reaction", "reaction_close"}:
        if str(continuity.get("screen_side", "") or "") != "actor":
            errors.append(f"{shot_id}: reaction shot should return continuity.screen_side to actor.")
        if not str(continuity.get("eyeline", "") or "").startswith("from_"):
            errors.append(f"{shot_id}: reaction shot should preserve eyeline from the previous object/screen.")
    if purpose in {"caller_close", "receiver_close"} and "to_" not in str(continuity.get("eyeline", "") or ""):
        errors.append(f"{shot_id}: speaker reverse coverage should declare eyeline toward the other speaker.")

    return errors


def as_number(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def as_offset(value) -> tuple[float, float] | None:
    if not isinstance(value, list) or len(value) != 2:
        return None
    x = as_number(value[0])
    y = as_number(value[1])
    if x is None or y is None:
        return None
    return x, y


def motion_plan_errors(shot: dict) -> list[str]:
    shot_id = shot.get("shot_id", "<unknown>")
    motion_plan = shot.get("motion_plan")
    if not isinstance(motion_plan, dict):
        return [f"{shot_id}: missing motion_plan block with style/start_scale/end_scale/start_offset/end_offset/easing/focus_shift/parallax."]

    errors: list[str] = []
    for key in sorted(MOTION_REQUIRED_FIELDS):
        if key not in motion_plan or motion_plan.get(key) in ("", None):
            errors.append(f"{shot_id}: missing motion_plan.{key}.")

    move = camera_field(shot, "move")
    style = str(motion_plan.get("style", "") or "")
    focus_shift = str(motion_plan.get("focus_shift", "") or "")
    parallax = str(motion_plan.get("parallax", "") or "")
    start_scale = as_number(motion_plan.get("start_scale"))
    end_scale = as_number(motion_plan.get("end_scale"))
    start_offset = as_offset(motion_plan.get("start_offset"))
    end_offset = as_offset(motion_plan.get("end_offset"))

    if start_scale is None:
        errors.append(f"{shot_id}: motion_plan.start_scale must be a number.")
    if end_scale is None:
        errors.append(f"{shot_id}: motion_plan.end_scale must be a number.")
    if start_offset is None:
        errors.append(f"{shot_id}: motion_plan.start_offset must be [x, y].")
    if end_offset is None:
        errors.append(f"{shot_id}: motion_plan.end_offset must be [x, y].")

    allowed_style_terms = MOVE_STYLE_PREFIX.get(move)
    if allowed_style_terms and style and not any(term in style for term in allowed_style_terms):
        errors.append(f"{shot_id}: camera.move '{move}' has mismatched motion_plan.style '{style}'.")

    if start_scale is not None and end_scale is not None and start_offset is not None and end_offset is not None:
        scale_delta = abs(end_scale - start_scale)
        offset_delta = abs(end_offset[0] - start_offset[0]) + abs(end_offset[1] - start_offset[1])
        if move in MOTION_MOVES and scale_delta < 0.01 and offset_delta < 4:
            errors.append(f"{shot_id}: moving camera '{move}' has no meaningful scale or offset change.")
        if move in STATIC_MOVES and (scale_delta >= 0.01 or offset_delta >= 4):
            errors.append(f"{shot_id}: static camera '{move}' should not include visible motion.")
        if start_scale <= 0 or end_scale <= 0:
            errors.append(f"{shot_id}: motion_plan scale values must be positive.")
        if start_scale > 1.35 or end_scale > 1.35:
            errors.append(f"{shot_id}: motion_plan scale exceeds 1.35, likely over-cropped for 2D collage.")

    if move in MOTION_MOVES and focus_shift == "none":
        errors.append(f"{shot_id}: moving camera '{move}' needs a non-none focus_shift.")
    if move in {"pan", "truck"} and parallax == "none":
        errors.append(f"{shot_id}: lateral camera '{move}' should declare subtle or layered parallax.")
    if move in STATIC_MOVES and focus_shift != "none":
        errors.append(f"{shot_id}: static camera '{move}' should use focus_shift 'none'.")
    return errors


def motion_is_visible(shot: dict) -> bool:
    motion_plan = shot.get("motion_plan")
    if not isinstance(motion_plan, dict):
        return False
    start_scale = as_number(motion_plan.get("start_scale"))
    end_scale = as_number(motion_plan.get("end_scale"))
    start_offset = as_offset(motion_plan.get("start_offset"))
    end_offset = as_offset(motion_plan.get("end_offset"))
    if start_scale is None or end_scale is None or start_offset is None or end_offset is None:
        return False
    scale_delta = abs(end_scale - start_scale)
    offset_delta = abs(end_offset[0] - start_offset[0]) + abs(end_offset[1] - start_offset[1])
    return scale_delta >= 0.01 or offset_delta >= 4


def motion_style(shot: dict) -> str:
    motion_plan = shot.get("motion_plan")
    if isinstance(motion_plan, dict):
        return str(motion_plan.get("style", "") or "")
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

    moving_count = sum(1 for s in shots if motion_is_visible(s))
    min_moving = max(2, round(runtime / 60 * 6))
    if moving_count < min_moving:
        errors.append(f"Visible camera motion too low: {moving_count}, expected at least {min_moving}.")

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
        errors.extend(directing_errors(shot))
        errors.extend(continuity_errors(shot))
        errors.extend(motion_plan_errors(shot))
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
        required_order = PATTERN_PURPOSE_ORDER.get(shot_pattern)
        if required_order:
            purpose_sequence = [str(s.get("purpose", "") or "") for s in event_shots]
            order_positions = [required_order.index(p) for p in purpose_sequence if p in required_order]
            if order_positions != sorted(order_positions):
                errors.append(f"{event_id}: {shot_pattern} purpose order is not cinematic: {' -> '.join(purpose_sequence)}.")

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
            event_moving_count = sum(1 for s in event_shots if motion_is_visible(s))
            event_motion_styles = {motion_style(s) for s in event_shots if motion_style(s)}
            event_motion_styles.discard("static_cut")
            if event_moving_count < 1:
                errors.append(f"{event_id}: event has no visible camera motion; add a motivated push, pull, pan, or track to change emphasis.")
            if len(event_shots) >= 4 and len(event_motion_styles) < 2:
                errors.append(f"{event_id}: event lacks non-static motion style variation; expected at least 2 moving styles in a longer beat.")

        for previous, current in zip(event_shots, event_shots[1:]):
            previous_role = str((previous.get("continuity") or {}).get("cut_role", "") or "")
            current_role = str((current.get("continuity") or {}).get("cut_role", "") or "")
            current_match = str((current.get("continuity") or {}).get("match", "") or "")
            current_id = current.get("shot_id", "<unknown>")
            if previous_role in {"contact", "transfer"} and current_role not in {"pov_reveal", "insert", "transfer", "reaction", "result"}:
                errors.append(f"{current_id}: shot after {previous_role} should reveal source, insert information, continue transfer, react, or show result.")
            if previous_role == "insert" and current_role in {"reaction", "reverse", "speaker"} and "_to_" not in current_match:
                errors.append(f"{current_id}: cut from insert to {current_role} should declare a directional match, got '{current_match}'.")
            if previous_role == "speaker" and current_role == "reverse" and current_match != "caller_to_receiver":
                errors.append(f"{current_id}: reverse speaker cut should match caller_to_receiver.")
            if previous_role == "reverse" and current_role == "bridge" and current_match != "two_sided_call":
                errors.append(f"{current_id}: bridge after reverse speaker cut should match two_sided_call.")

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
