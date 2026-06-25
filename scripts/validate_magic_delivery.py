from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "magic-delivery"
SHOT_FILE = PROJECT / "shots" / "climax_60s.json"

REQUIRED_FIELDS = {
    "shot_id",
    "duration",
    "location",
    "beat",
    "characters",
    "action",
    "expression",
    "speaker",
    "dialogue",
    "ui",
    "vfx",
    "vfx_reason",
    "transition",
    "camera",
    "assets",
}

KNOWN_ACTIONS = {
    "scooter_enter",
    "hand_food_bag",
    "shocked_recoil",
    "system_popup",
    "phone_tap",
    "proof_photo",
    "voice_appeal",
    "block_with_bag",
    "route_recalc",
    "confirm_button",
    "eat_and_review",
    "phone_closeup",
}

KNOWN_EXPRESSIONS = {
    "determined_sweat",
    "neutral_to_smirk",
    "shocked",
    "comic_panic",
    "serious",
    "heroic_resolve",
    "angry_panic",
    "soft_realization",
    "blank",
}

KNOWN_TRANSITIONS = {
    "impact_cut",
    "subtitle_slam",
    "cut",
    "glitch_realm_shift",
    "whip_pan",
    "smoke_wipe_fast",
    "match_cut_prop",
    "cut_to_black",
}

KNOWN_CAMERA_PRESETS = {
    "establishing_pan",
    "push_in",
    "pull_back",
    "truck_left",
    "truck_right",
    "over_shoulder",
    "insert_closeup",
    "reaction_cut",
    "static_hold",
}

KNOWN_FRAMING = {"wide", "medium", "closeup", "insert"}

FORBIDDEN_TRANSITIONS = {
    "impact_flash_cut": "Use impact_cut; do not combine default flash with shake.",
    "hard_cut": "Use cut.",
}


def main() -> int:
    errors: list[str] = []
    data = json.loads(SHOT_FILE.read_text(encoding="utf-8"))
    shots = data.get("shots", [])

    if not shots:
        errors.append("No shots found.")

    total = sum(float(shot.get("duration", 0)) for shot in shots)
    if abs(total - 60) > 0.01:
        errors.append(f"Expected 60 seconds, got {total}.")

    fmt = data.get("format", {})
    if fmt.get("width") != 1920 or fmt.get("height") != 1080:
        errors.append(f"Expected horizontal 1920x1080 format, got {fmt}.")
    if data.get("aspect") not in {None, "16:9"}:
        errors.append(f"Expected 16:9 aspect, got {data.get('aspect')}.")

    camera_pairs: list[tuple[str, str]] = []
    framing_types: set[str] = set()

    for index, shot in enumerate(shots, 1):
        shot_id = shot.get("shot_id", f"#{index}")
        missing = REQUIRED_FIELDS - set(shot)
        if missing:
            errors.append(f"{shot_id} missing fields: {', '.join(sorted(missing))}")
        if shot.get("action") not in KNOWN_ACTIONS:
            errors.append(f"{shot_id} unknown action: {shot.get('action')}")
        if shot.get("expression") not in KNOWN_EXPRESSIONS:
            errors.append(f"{shot_id} unknown expression: {shot.get('expression')}")
        if shot.get("transition") not in KNOWN_TRANSITIONS:
            errors.append(f"{shot_id} unknown transition: {shot.get('transition')}")
        if shot.get("transition") in FORBIDDEN_TRANSITIONS:
            errors.append(f"{shot_id} forbidden transition {shot.get('transition')}: {FORBIDDEN_TRANSITIONS[shot.get('transition')]}")
        if len(str(shot.get("dialogue", ""))) > 42:
            print(f"Warning: {shot_id} dialogue may need subtitle wrapping.")
        camera = shot.get("camera")
        if not isinstance(camera, dict):
            errors.append(f"{shot_id} missing camera block.")
        else:
            preset = camera.get("preset")
            framing = camera.get("framing")
            if preset not in KNOWN_CAMERA_PRESETS:
                errors.append(f"{shot_id} unknown camera preset: {preset}")
            if framing not in KNOWN_FRAMING:
                errors.append(f"{shot_id} unknown camera framing: {framing}")
            intensity = float(camera.get("motion_intensity", 0))
            if intensity < 0 or intensity > 0.75:
                errors.append(f"{shot_id} camera motion_intensity must be 0..0.75, got {intensity}")
            camera_pairs.append((str(preset), str(framing)))
            framing_types.add(str(framing))
        if shot.get("vfx") != "none" and not str(shot.get("vfx_reason", "")).strip():
            errors.append(f"{shot_id} has active VFX but no vfx_reason.")
        assets = shot.get("assets")
        if not isinstance(assets, dict):
            errors.append(f"{shot_id} missing assets block.")
        else:
            if not assets.get("required"):
                errors.append(f"{shot_id} assets.required is empty.")
            if not str(assets.get("fallback", "")).strip():
                errors.append(f"{shot_id} assets.fallback is required.")

    camera_changes = sum(1 for a, b in zip(camera_pairs, camera_pairs[1:]) if a != b)
    if camera_changes < 5:
        errors.append(f"Expected at least 5 camera/framing changes, got {camera_changes}.")
    if len(framing_types) < 3:
        errors.append(f"Expected at least 3 framing types, got {sorted(framing_types)}.")

    for path in [
        PROJECT / "docs" / "00_Project_Bible.md",
        PROJECT / "docs" / "01_Story_Outline.md",
        PROJECT / "docs" / "02_Scene_List.md",
        PROJECT / "workflow" / "asset_pipeline.yaml",
        PROJECT / "workflow" / "edit_presets.yaml",
        PROJECT / "assets" / "00_license_records" / "asset_manifest.csv",
    ]:
        if not path.exists():
            errors.append(f"Missing workflow file: {path}")

    if errors:
        print("Magic delivery validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Magic delivery validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
