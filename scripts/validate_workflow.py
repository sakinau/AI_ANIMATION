from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def expect_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        fail(f"Missing file: {path}", errors)


def main() -> int:
    errors: list[str] = []
    story = read_json(ROOT / "project" / "story.json")
    presets = read_json(ROOT / "project" / "animation-presets.json")
    calibration = read_json(ROOT / "project" / "asset-calibration.json")

    actions = set(presets["poseBeats"])
    expressions = set(presets["expressionBeats"])
    pose_names = set(calibration["poses"])

    for scene in story["scenes"]:
        action = scene["action"]
        expression = scene["expression"]
        if action not in actions:
            fail(f"{scene['id']} uses action without pose preset: {action}", errors)
        if expression not in expressions:
            fail(f"{scene['id']} uses expression without expression preset: {expression}", errors)
        if action in presets["actionMotion"] and presets["actionMotion"][action] not in presets["motions"]:
            fail(f"{scene['id']} uses missing motion preset: {presets['actionMotion'][action]}", errors)

    for action, poses in presets["poseBeats"].items():
        for pose in poses:
            if pose not in pose_names:
                fail(f"Action {action} references pose without calibration: {pose}", errors)
            expect_file(
                PUBLIC / "免费素材库" / "处理后" / "人物" / "橙衣男" / f"橙衣男-{pose}.png",
                errors,
            )

    for name in [
        "表情-平静.png",
        "表情-怀疑.png",
        "表情-恐惧.png",
        "表情-惊讶.png",
        "表情-悲伤.png",
        "表情-邪笑.png",
    ]:
        expect_file(PUBLIC / "免费素材库" / "处理后" / "表情" / name, errors)

    story_tsx = (ROOT / "src" / "Story.tsx").read_text(encoding="utf-8")
    forbidden = ["transition:", "animation:", "@keyframes"]
    for token in forbidden:
        if token in story_tsx:
            fail(f"Remotion code contains forbidden CSS animation token: {token}", errors)

    if errors:
        print("Workflow validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Workflow validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
