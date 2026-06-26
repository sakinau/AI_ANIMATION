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
        if not (event_types & INTERACTION_TYPES or "interaction" in event_types):
            continue
        purposes = " ".join(str(s.get("purpose", "") or "").lower() for s in event_shots)
        framings = {camera_field(s, "framing") for s in event_shots}
        motivations = {camera_field(s, "motivation") for s in event_shots}
        has_insert = bool(framings & {"insert", "closeup", "extreme_closeup"})
        has_contact = "contact" in purposes or "show_contact" in motivations
        has_reaction = "reaction" in purposes or "show_reaction" in motivations
        if len(event_shots) < 2:
            errors.append(f"{event_id}: interaction event has only one shot.")
        if not has_insert:
            errors.append(f"{event_id}: interaction event lacks insert/closeup coverage.")
        if ("object_pickup" in event_types or "interaction" in event_types) and not has_contact:
            errors.append(f"{event_id}: pickup/contact event lacks contact coverage.")
        if ("screen_discovery" in event_types or "phone_call" in event_types) and not has_reaction:
            errors.append(f"{event_id}: discovery/call event lacks reaction coverage.")

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
