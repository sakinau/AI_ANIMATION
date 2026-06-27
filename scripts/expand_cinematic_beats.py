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
            "edit": {"transition": "scene_start", "continuity": "establish_context", "reason": "orient audience before information insert"},
        },
        {
            "suffix": "02",
            "event_type": "screen_discovery",
            "purpose": "screen_insert",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "cut", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "look_to_object", "reason": "make the discovered screen readable"},
        },
        {
            "suffix": "03",
            "event_type": "reaction",
            "purpose": "reaction_close",
            "duration": 3,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
            "edit": {"transition": "reaction_cut", "continuity": "object_to_reaction", "reason": "show why the information matters"},
        },
    ],
    "object_pickup_sequence": [
        {
            "suffix": "01",
            "purpose": "approach_object",
            "duration": 4,
            "camera": {"angle": "side", "framing": "medium", "lens": "normal", "move": "truck", "motivation": "establish_space"},
            "edit": {"transition": "action_start", "continuity": "screen_direction", "reason": "establish actor route to the object"},
        },
        {
            "suffix": "02",
            "purpose": "contact",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "extreme_closeup", "lens": "telephoto", "move": "cut", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "hand_to_contact", "reason": "cut from approach to the exact contact point"},
        },
        {
            "suffix": "03",
            "purpose": "reveal_source",
            "duration": 4,
            "camera": {"angle": "pov", "framing": "insert", "lens": "wide", "move": "pull_back", "motivation": "reveal_object"},
            "edit": {"transition": "pov_cut", "continuity": "contact_to_source", "reason": "show what is inside or behind the contacted object"},
        },
        {
            "suffix": "04",
            "purpose": "show_pickup",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "extreme_closeup", "lens": "telephoto", "move": "cut", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "source_to_hand", "reason": "compress the detailed pickup into a clear contact insert"},
        },
        {
            "suffix": "05",
            "event_type": "reaction",
            "purpose": "reaction",
            "duration": 3,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
            "edit": {"transition": "reaction_cut", "continuity": "object_to_reaction", "reason": "show the character response after pickup"},
        },
        {
            "suffix": "06",
            "purpose": "result_insert",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_result"},
            "edit": {"transition": "result_cut", "continuity": "reaction_to_result", "reason": "confirm the post-action object state"},
        },
    ],
    "object_putdown_sequence": [
        {
            "suffix": "01",
            "purpose": "contact",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "push_in", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "hand_to_surface", "reason": "show contact with the destination surface"},
        },
        {
            "suffix": "02",
            "purpose": "result_insert",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_result"},
            "edit": {"transition": "result_cut", "continuity": "contact_to_result", "reason": "show the completed placed state"},
        },
    ],
    "watch_screen_discovery": [
        {
            "suffix": "01",
            "purpose": "actor_context",
            "duration": 4,
            "camera": {"angle": "eye_level", "framing": "medium", "lens": "normal", "move": "cut", "motivation": "establish_space"},
            "edit": {"transition": "context_cut", "continuity": "actor_context", "reason": "show what the actor is doing before discovery"},
        },
        {
            "suffix": "02",
            "purpose": "screen_insert",
            "duration": 4,
            "camera": {"angle": "pov", "framing": "insert", "lens": "telephoto", "move": "push_in", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "look_to_screen", "reason": "make screen information readable"},
        },
        {
            "suffix": "03",
            "purpose": "reaction_close",
            "duration": 3,
            "camera": {"angle": "low_angle", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
            "edit": {"transition": "reaction_cut", "continuity": "screen_to_reaction", "reason": "show the decision beat after screen discovery"},
        },
    ],
    "phone_call": [
        {
            "suffix": "01",
            "event_type": "object_pickup",
            "purpose": "pickup_phone",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "hand_to_phone", "reason": "show how the call begins"},
        },
        {
            "suffix": "02",
            "event_type": "phone_call",
            "purpose": "dial_screen",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "cut", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "phone_to_screen", "reason": "show the dialing state before dialogue"},
        },
        {
            "suffix": "03",
            "event_type": "phone_call",
            "purpose": "caller_close",
            "duration": 4,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "cut", "motivation": "show_reaction"},
            "edit": {"transition": "speaker_cut", "continuity": "screen_to_caller", "reason": "move from call setup to caller line"},
        },
        {
            "suffix": "04",
            "event_type": "phone_call",
            "purpose": "receiver_close",
            "duration": 4,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "cut", "motivation": "show_reaction"},
            "edit": {"transition": "reverse_cut", "continuity": "caller_to_receiver", "reason": "cut to response speaker"},
        },
        {
            "suffix": "05",
            "event_type": "phone_call",
            "purpose": "split_result",
            "duration": 5,
            "camera": {"angle": "front", "framing": "medium", "lens": "normal", "move": "cut", "motivation": "show_result"},
            "edit": {"transition": "split_screen_bridge", "continuity": "two_sided_call", "reason": "summarize the shared decision"},
        },
    ],
    "meeting_at_location": [
        {
            "suffix": "01",
            "event_type": "meeting",
            "purpose": "location_establish",
            "duration": 4,
            "camera": {"angle": "high_angle", "framing": "wide", "lens": "wide", "move": "pan", "motivation": "establish_space"},
            "edit": {"transition": "time_cut", "continuity": "new_location", "reason": "jump to the meeting location after the call"},
        },
        {
            "suffix": "02",
            "event_type": "meeting",
            "purpose": "counterpart_reveal",
            "duration": 4,
            "camera": {"angle": "over_shoulder", "framing": "medium", "lens": "normal", "move": "truck", "motivation": "reveal_object"},
            "edit": {"transition": "reveal_cut", "continuity": "arrival_to_counterpart", "reason": "reveal the other character from the first character's side"},
        },
        {
            "suffix": "03",
            "event_type": "screen_discovery",
            "purpose": "event_notice_insert",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "push_in", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "counterpart_to_notice", "reason": "show the sign that motivates the meeting"},
        },
        {
            "suffix": "04",
            "event_type": "meeting",
            "purpose": "reaction_pair_result",
            "duration": 4,
            "camera": {"angle": "eye_level", "framing": "medium", "lens": "normal", "move": "pull_back", "motivation": "show_reaction"},
            "edit": {"transition": "result_cut", "continuity": "notice_to_pair", "reason": "return to the pair and complete the beat"},
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
            "edit": deepcopy(phase.get("edit", {})),
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
        "subject_registry": deepcopy(data.get("subject_registry", {})),
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
