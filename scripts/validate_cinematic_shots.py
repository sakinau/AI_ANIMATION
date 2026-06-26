import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


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


def load_sequence(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


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


def validate(path: Path) -> list[str]:
    data = load_sequence(path)
    shots = data.get("shots", [])
    errors: list[str] = []
    warnings: list[str] = []

    if not shots:
        return ["No shots found."]

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
