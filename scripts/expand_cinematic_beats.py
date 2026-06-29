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
            "continuity": {"screen_side": "neutral", "eyeline": "none", "match": "establish_context", "cut_role": "establish"},
        },
        {
            "suffix": "02",
            "event_type": "screen_discovery",
            "purpose": "screen_insert",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "cut", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "look_to_object", "reason": "make the discovered screen readable"},
            "continuity": {"screen_side": "object", "eyeline": "target", "match": "look_to_object", "cut_role": "insert"},
        },
        {
            "suffix": "03",
            "event_type": "reaction",
            "purpose": "reaction_close",
            "duration": 3,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
            "edit": {"transition": "reaction_cut", "continuity": "object_to_reaction", "reason": "show why the information matters"},
            "continuity": {"screen_side": "actor", "eyeline": "from_object", "match": "object_to_reaction", "cut_role": "reaction"},
        },
    ],
    "object_pickup_sequence": [
        {
            "suffix": "01",
            "purpose": "approach_object",
            "duration": 4,
            "camera": {"angle": "side", "framing": "medium", "lens": "normal", "move": "truck", "motivation": "establish_space"},
            "edit": {"transition": "action_start", "continuity": "screen_direction", "reason": "establish actor route to the object"},
            "continuity": {"screen_side": "actor_left_to_right", "eyeline": "toward_object", "match": "screen_direction", "cut_role": "action_start"},
        },
        {
            "suffix": "02",
            "purpose": "contact",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "extreme_closeup", "lens": "telephoto", "move": "cut", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "hand_to_contact", "reason": "cut from approach to the exact contact point"},
            "continuity": {"screen_side": "object", "eyeline": "none", "match": "hand_to_contact", "cut_role": "contact"},
        },
        {
            "suffix": "03",
            "purpose": "reveal_source",
            "duration": 4,
            "camera": {"angle": "pov", "framing": "insert", "lens": "wide", "move": "pull_back", "motivation": "reveal_object"},
            "edit": {"transition": "pov_cut", "continuity": "contact_to_source", "reason": "show what is inside or behind the contacted object"},
            "continuity": {"screen_side": "object", "eyeline": "pov", "match": "contact_to_source", "cut_role": "pov_reveal"},
        },
        {
            "suffix": "04",
            "purpose": "show_pickup",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "extreme_closeup", "lens": "telephoto", "move": "cut", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "source_to_hand", "reason": "compress the detailed pickup into a clear contact insert"},
            "continuity": {"screen_side": "object", "eyeline": "none", "match": "source_to_hand", "cut_role": "transfer"},
        },
        {
            "suffix": "05",
            "event_type": "reaction",
            "purpose": "reaction",
            "duration": 3,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
            "edit": {"transition": "reaction_cut", "continuity": "object_to_reaction", "reason": "show the character response after pickup"},
            "continuity": {"screen_side": "actor", "eyeline": "from_object", "match": "object_to_reaction", "cut_role": "reaction"},
        },
        {
            "suffix": "06",
            "purpose": "result_insert",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_result"},
            "edit": {"transition": "result_cut", "continuity": "reaction_to_result", "reason": "confirm the post-action object state"},
            "continuity": {"screen_side": "object", "eyeline": "none", "match": "reaction_to_result", "cut_role": "result"},
        },
    ],
    "object_putdown_sequence": [
        {
            "suffix": "01",
            "purpose": "contact",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "push_in", "motivation": "show_contact"},
            "edit": {"transition": "action_match_cut", "continuity": "hand_to_surface", "reason": "show contact with the destination surface"},
            "continuity": {"screen_side": "object", "eyeline": "none", "match": "hand_to_surface", "cut_role": "contact"},
        },
        {
            "suffix": "02",
            "purpose": "result_insert",
            "duration": 3,
            "camera": {"angle": "high_angle", "framing": "insert", "lens": "normal", "move": "cut", "motivation": "show_result"},
            "edit": {"transition": "result_cut", "continuity": "contact_to_result", "reason": "show the completed placed state"},
            "continuity": {"screen_side": "object", "eyeline": "none", "match": "contact_to_result", "cut_role": "result"},
        },
    ],
    "watch_screen_discovery": [
        {
            "suffix": "01",
            "purpose": "actor_context",
            "duration": 4,
            "camera": {"angle": "eye_level", "framing": "medium", "lens": "normal", "move": "cut", "motivation": "establish_space"},
            "edit": {"transition": "context_cut", "continuity": "actor_context", "reason": "show what the actor is doing before discovery"},
            "continuity": {"screen_side": "actor", "eyeline": "toward_screen", "match": "actor_context", "cut_role": "context"},
        },
        {
            "suffix": "02",
            "purpose": "screen_insert",
            "duration": 4,
            "camera": {"angle": "pov", "framing": "insert", "lens": "telephoto", "move": "push_in", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "look_to_screen", "reason": "make screen information readable"},
            "continuity": {"screen_side": "object", "eyeline": "pov", "match": "look_to_screen", "cut_role": "insert"},
        },
        {
            "suffix": "03",
            "purpose": "reaction_close",
            "duration": 3,
            "camera": {"angle": "low_angle", "framing": "closeup", "lens": "telephoto", "move": "push_in", "motivation": "show_reaction"},
            "edit": {"transition": "reaction_cut", "continuity": "screen_to_reaction", "reason": "show the decision beat after screen discovery"},
            "continuity": {"screen_side": "actor", "eyeline": "from_screen", "match": "screen_to_reaction", "cut_role": "reaction"},
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
            "continuity": {"screen_side": "object", "eyeline": "none", "match": "hand_to_phone", "cut_role": "contact"},
        },
        {
            "suffix": "02",
            "event_type": "phone_call",
            "purpose": "dial_screen",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "cut", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "phone_to_screen", "reason": "show the dialing state before dialogue"},
            "continuity": {"screen_side": "object", "eyeline": "target", "match": "phone_to_screen", "cut_role": "insert"},
        },
        {
            "suffix": "03",
            "event_type": "phone_call",
            "purpose": "caller_close",
            "duration": 4,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "cut", "motivation": "show_reaction"},
            "edit": {"transition": "speaker_cut", "continuity": "screen_to_caller", "reason": "move from call setup to caller line"},
            "continuity": {"screen_side": "caller", "eyeline": "to_receiver", "match": "screen_to_caller", "cut_role": "speaker"},
        },
        {
            "suffix": "04",
            "event_type": "phone_call",
            "purpose": "receiver_close",
            "duration": 4,
            "camera": {"angle": "front", "framing": "closeup", "lens": "telephoto", "move": "cut", "motivation": "show_reaction"},
            "edit": {"transition": "reverse_cut", "continuity": "caller_to_receiver", "reason": "cut to response speaker"},
            "continuity": {"screen_side": "receiver", "eyeline": "to_caller", "match": "caller_to_receiver", "cut_role": "reverse"},
        },
        {
            "suffix": "05",
            "event_type": "phone_call",
            "purpose": "split_result",
            "duration": 5,
            "camera": {"angle": "front", "framing": "medium", "lens": "normal", "move": "cut", "motivation": "show_result"},
            "edit": {"transition": "split_screen_bridge", "continuity": "two_sided_call", "reason": "summarize the shared decision"},
            "continuity": {"screen_side": "split", "eyeline": "paired", "match": "two_sided_call", "cut_role": "bridge"},
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
            "continuity": {"screen_side": "neutral", "eyeline": "none", "match": "new_location", "cut_role": "establish"},
        },
        {
            "suffix": "02",
            "event_type": "meeting",
            "purpose": "counterpart_reveal",
            "duration": 4,
            "camera": {"angle": "over_shoulder", "framing": "medium", "lens": "normal", "move": "truck", "motivation": "reveal_object"},
            "edit": {"transition": "reveal_cut", "continuity": "arrival_to_counterpart", "reason": "reveal the other character from the first character's side"},
            "continuity": {"screen_side": "counterpart", "eyeline": "from_actor", "match": "arrival_to_counterpart", "cut_role": "reveal"},
        },
        {
            "suffix": "03",
            "event_type": "screen_discovery",
            "purpose": "event_notice_insert",
            "duration": 3,
            "camera": {"angle": "insert", "framing": "insert", "lens": "telephoto", "move": "push_in", "motivation": "reveal_object"},
            "edit": {"transition": "insert_cut", "continuity": "counterpart_to_notice", "reason": "show the sign that motivates the meeting"},
            "continuity": {"screen_side": "object", "eyeline": "target", "match": "counterpart_to_notice", "cut_role": "insert"},
        },
        {
            "suffix": "04",
            "event_type": "meeting",
            "purpose": "reaction_pair_result",
            "duration": 4,
            "camera": {"angle": "eye_level", "framing": "medium", "lens": "normal", "move": "pull_back", "motivation": "show_reaction"},
            "edit": {"transition": "result_cut", "continuity": "notice_to_pair", "reason": "return to the pair and complete the beat"},
            "continuity": {"screen_side": "pair", "eyeline": "shared", "match": "notice_to_pair", "cut_role": "result"},
        },
    ],
}


PURPOSE_DIRECTING: dict[str, dict] = {
    "establish_space": {
        "action_phase": "setup",
        "focus": "space_before_subject",
        "composition": "geography_first",
        "emphasis": "orient the audience before the gag or action",
    },
    "screen_insert": {
        "action_phase": "information",
        "focus": "readable_screen",
        "composition": "object_fills_frame",
        "emphasis": "make the discovered information readable",
    },
    "reaction_close": {
        "action_phase": "reaction",
        "focus": "face_or_body_reaction",
        "composition": "character_close_priority",
        "emphasis": "show why the previous information matters",
    },
    "approach_object": {
        "action_phase": "approach",
        "focus": "actor_route_to_object",
        "composition": "screen_direction_visible",
        "emphasis": "show the path before contact",
    },
    "contact": {
        "action_phase": "contact",
        "focus": "hand_or_object_contact",
        "composition": "contact_point_priority",
        "emphasis": "sell the physical touch or placement",
    },
    "reveal_source": {
        "action_phase": "source_reveal",
        "focus": "object_source",
        "composition": "pov_or_insert_reveal",
        "emphasis": "show what is being chosen or discovered",
    },
    "show_pickup": {
        "action_phase": "transfer",
        "focus": "object_transfer",
        "composition": "object_and_hand_priority",
        "emphasis": "make the pickup feel intentional, not floating",
    },
    "reaction": {
        "action_phase": "reaction",
        "focus": "face_or_body_reaction",
        "composition": "character_close_priority",
        "emphasis": "punctuate the action with character attitude",
    },
    "result_insert": {
        "action_phase": "result",
        "focus": "post_action_object_state",
        "composition": "result_state_centered",
        "emphasis": "confirm where the object ended up",
    },
    "actor_context": {
        "action_phase": "setup",
        "focus": "actor_previous_activity",
        "composition": "actor_with_relevant_prop",
        "emphasis": "show what the actor is doing before the discovery",
    },
    "pickup_phone": {
        "action_phase": "contact",
        "focus": "phone_contact",
        "composition": "hand_and_phone_insert",
        "emphasis": "show how the call begins",
    },
    "dial_screen": {
        "action_phase": "information",
        "focus": "phone_screen_state",
        "composition": "screen_fills_frame",
        "emphasis": "show the call state before dialogue",
    },
    "caller_close": {
        "action_phase": "speaker",
        "focus": "caller_performance",
        "composition": "speaker_close_priority",
        "emphasis": "make the caller's line readable as performance",
    },
    "receiver_close": {
        "action_phase": "reverse_speaker",
        "focus": "receiver_performance",
        "composition": "reverse_close_priority",
        "emphasis": "cut to the answer instead of holding one side",
    },
    "split_result": {
        "action_phase": "shared_result",
        "focus": "two_sided_decision",
        "composition": "split_or_two_panel_balance",
        "emphasis": "summarize the shared decision",
    },
    "location_establish": {
        "action_phase": "setup",
        "focus": "new_location_geography",
        "composition": "wide_geography_with_signage",
        "emphasis": "orient the audience after a time or location jump",
    },
    "counterpart_reveal": {
        "action_phase": "reveal",
        "focus": "second_character_entrance",
        "composition": "over_shoulder_or_side_reveal",
        "emphasis": "reveal the other character from a motivated viewpoint",
    },
    "event_notice_insert": {
        "action_phase": "information",
        "focus": "readable_notice",
        "composition": "sign_or_notice_fills_frame",
        "emphasis": "show the detail that motivates the next reaction",
    },
    "reaction_pair_result": {
        "action_phase": "shared_reaction",
        "focus": "pair_result",
        "composition": "two_shot_result",
        "emphasis": "return to the characters and complete the beat",
    },
}

MOVE_PLANS: dict[str, dict] = {
    "cut": {
        "style": "static_cut",
        "start_scale": 1.0,
        "end_scale": 1.0,
        "start_offset": [0, 0],
        "end_offset": [0, 0],
        "easing": "hold",
        "focus_shift": "none",
        "parallax": "none",
    },
    "push_in": {
        "style": "motivated_push",
        "start_scale": 1.0,
        "end_scale": 1.08,
        "start_offset": [0, 0],
        "end_offset": [0, -18],
        "easing": "ease_out",
        "focus_shift": "toward_subject",
        "parallax": "subtle",
    },
    "pull_back": {
        "style": "reveal_pull",
        "start_scale": 1.08,
        "end_scale": 1.0,
        "start_offset": [0, -16],
        "end_offset": [0, 0],
        "easing": "ease_in_out",
        "focus_shift": "subject_to_space",
        "parallax": "subtle",
    },
    "pan": {
        "style": "geography_pan",
        "start_scale": 1.05,
        "end_scale": 1.05,
        "start_offset": [-80, 0],
        "end_offset": [80, 0],
        "easing": "ease_in_out",
        "focus_shift": "scan_space",
        "parallax": "layered",
    },
    "truck": {
        "style": "lateral_track",
        "start_scale": 1.03,
        "end_scale": 1.03,
        "start_offset": [-70, 0],
        "end_offset": [70, 0],
        "easing": "linear_soft",
        "focus_shift": "follow_subject",
        "parallax": "layered",
    },
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def phase_value(event: dict, key: str, purpose: str, default=None):
    values = event.get(key, {})
    if isinstance(values, dict):
        return values.get(purpose, default)
    return default


def phase_directing(event: dict, phase: dict, purpose: str) -> dict:
    directing = deepcopy(PURPOSE_DIRECTING.get(purpose, {}))
    directing.update(deepcopy(phase.get("directing", {})))
    directing.update(deepcopy(phase_value(event, "directing", purpose, {})))
    return directing


def phase_continuity(event: dict, phase: dict, purpose: str) -> dict:
    continuity = deepcopy(phase.get("continuity", {}))
    continuity.update(deepcopy(phase_value(event, "continuity", purpose, {})))
    return continuity


def phase_motion_plan(event: dict, phase: dict, purpose: str) -> dict:
    move = str((phase.get("camera") or {}).get("move", "") or "cut")
    plan = deepcopy(MOVE_PLANS.get(move, MOVE_PLANS["cut"]))
    plan.update(deepcopy(phase.get("motion_plan", {})))
    plan.update(deepcopy(phase_value(event, "motion_plan", purpose, {})))
    return plan


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
            "directing": phase_directing(event, phase, purpose),
            "continuity": phase_continuity(event, phase, purpose),
            "motion_plan": phase_motion_plan(event, phase, purpose),
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
        "action_registry": deepcopy(data.get("action_registry", {})),
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
