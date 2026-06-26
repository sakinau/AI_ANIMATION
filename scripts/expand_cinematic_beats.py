import argparse
import json
from copy import deepcopy
from pathlib import Path


PATTERNS: dict[str, list[dict]] = {
    "establish_to_reaction": [
        {
            "suffix": "01",
            "event_type": "establish",
            "purpose": "establish_space",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "wide", "lens": "wide", "move": "push_in", "motivation": "establish_space"},
        },
        {
            "suffix": "02",
            "event_type": "screen_discovery",
            "purpose": "screen_insert",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "cut", "motivation": "reveal_object"},
        },
        {
            "suffix": "03",
            "event_type": "reaction",
            "purpose": "reaction_close",
            "duration": 3,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
        },
    ],
    "object_pickup_sequence": [
        {
            "suffix": "01",
            "purpose": "approach_object",
            "duration": 4,
            "camera": {"angle": "side", "framing": "medium", "lens": "normal", "move": "truck", "motivation": "establish_space"},
        },
        {
            "suffix": "02",
            "purpose": "contact",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "extreme_closeup", "lens": "telephoto", "move": "cut", "motivation": "show_contact"},
        },
        {
            "suffix": "03",
            "purpose": "reveal_source",
            "duration": 4,
            "camera": {"angle": "pov", "framing": "insert", "lens": "wide", "move": "pull_back", "motivation": "reveal_object"},
        },
        {
            "suffix": "04",
            "purpose": "show_pickup",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "extreme_closeup", "lens": "telephoto", "move": "cut", "motivation": "show_contact"},
        },
        {
            "suffix": "05",
            "event_type": "reaction",
            "purpose": "reaction",
            "duration": 3,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
        },
    ],
    "object_putdown_sequence": [
        {
            "suffix": "01",
            "purpose": "contact",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "push_in", "motivation": "show_contact"},
        },
        {
            "suffix": "02",
            "purpose": "result_insert",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_result"},
        },
    ],
    "watch_screen_discovery": [
        {
            "suffix": "01",
            "purpose": "actor_context",
            "duration": 4,
            "camera": {"angle": "eye_level", "framing": "medium", "lens": "normal", "move": "cut", "motivation": "establish_space"},
        },
        {
            "suffix": "02",
            "purpose": "screen_insert",
            "duration": 4,
            "camera": {"angle": "pov", "framing": "insert", "lens": "telephoto", "move": "push_in", "motivation": "reveal_object"},
        },
        {
            "suffix": "03",
            "purpose": "reaction_close",
            "duration": 3,
            "camera": {"angle": "low_angle", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
        },
    ],
    "phone_call": [
        {
            "suffix": "01",
            "event_type": "object_pickup",
            "purpose": "pickup_phone",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_contact"},
        },
        {
            "suffix": "02",
            "event_type": "phone_call",
            "purpose": "dial_screen",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "cut", "motivation": "reveal_object"},
        },
        {
            "suffix": "03",
            "event_type": "phone_call",
            "purpose": "caller_close",
            "duration": 4,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "cut", "motivation": "show_reaction"},
        },
        {
            "suffix": "04",
            "event_type": "phone_call",
            "purpose": "receiver_close",
            "duration": 4,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "cut", "motivation": "show_reaction"},
        },
        {
            "suffix": "05",
            "event_type": "phone_call",
            "purpose": "split_result",
            "duration": 5,
            "camera": {"angle": "front", "framing": "medium", "lens": "normal", "move": "cut", "motivation": "show_result"},
        },
    ],
    "meeting_at_location": [
        {
            "suffix": "01",
            "event_type": "meeting",
            "purpose": "location_establish",
            "duration": 4,
            "camera": {"angle": "high_angle", "framing": "wide", "lens": "wide", "move": "pan", "motivation": "establish_space"},
        },
        {
            "suffix": "02",
            "event_type": "meeting",
            "purpose": "counterpart_reveal",
            "duration": 4,
            "camera": {"angle": "over_shoulder", "framing": "medium", "lens": "normal", "move": "truck", "motivation": "reveal_object"},
        },
        {
            "suffix": "03",
            "event_type": "screen_discovery",
            "purpose": "event_notice_insert",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "push_in", "motivation": "reveal_object"},
        },
        {
            "suffix": "04",
            "event_type": "meeting",
            "purpose": "reaction_pair_result",
            "duration": 4,
            "camera": {"angle": "eye_level", "framing": "medium", "lens": "normal", "move": "pull_back", "motivation": "show_reaction"},
        },
    ],
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def phase_value(event: dict, key: str, purpose: str, default=None):
    values = event.get(key, {})
    if isinstance(values, dict):
        return values.get(purpose, default)
    return default


def expand_event(event: dict, event_index: int) -> list[dict]:
    pattern_name = event["shot_pattern"]
    if pattern_name not in PATTERNS:
        raise ValueError(f"Unknown shot_pattern: {pattern_name}")

    shots = []
    for phase in PATTERNS[pattern_name]:
        purpose = phase["purpose"]
        shot = {
            "shot_id": f"{event.get('shot_prefix', f'E{event_index:02d}')}{phase['suffix']}",
            "event_id": event["event_id"],
            "event_type": phase.get("event_type", event["event_type"]),
            "shot_pattern": pattern_name,
            "purpose": purpose,
            "duration": phase_value(event, "durations", purpose, phase["duration"]),
            "scene_pack": phase_value(event, "scene_packs", purpose, event["scene_pack"]),
            "background": phase_value(event, "backgrounds", purpose, event.get("background", "wide")),
            "action": phase_value(event, "actions", purpose, purpose),
            "dialogue": phase_value(event, "dialogue", purpose, event.get("dialogue", "")),
            "camera": deepcopy(phase["camera"]),
        }
        subject = phase_value(event, "subjects", purpose, event.get("subject"))
        if subject:
            shot["camera"]["subject"] = subject
        if "blocking" in event:
            shot["blocking"] = deepcopy(event["blocking"])
        if "interaction" in event:
            shot["interaction"] = deepcopy(event["interaction"])
        shots.append(shot)
    return shots


def expand_sequence(data: dict) -> dict:
    out = {
        "project_id": data["project_id"],
        "sequence_id": data["sequence_id"],
        "title": data.get("title", data["sequence_id"]),
        "fps": data.get("fps", 12),
        "format": data.get("format", {"width": 1920, "height": 1080}),
        "goal": data.get("goal", "Generated cinematic shot list from event beats."),
        "source_events": data.get("source_events", ""),
        "shots": [],
    }
    for index, event in enumerate(data.get("events", []), start=1):
        out["shots"].extend(expand_event(event, index))
    out["runtime_seconds"] = sum(float(shot.get("duration", 0)) for shot in out["shots"])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand cinematic story events into validated shot-list JSON.")
    parser.add_argument("events_json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    data = read_json(args.events_json)
    out = expand_sequence(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print(f"Wrote {len(out['shots'])} shots, {out['runtime_seconds']:g}s: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
