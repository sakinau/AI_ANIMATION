import argparse
import sys
from pathlib import Path

import yaml


REQUIRED_TOP = {
    "scene_id",
    "name",
    "format",
    "backgrounds",
    "layers",
    "anchors",
    "props",
    "supported_actions",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def iter_paths(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_paths(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_paths(item)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scene_pack", help="Path to scene pack folder or scene.yaml")
    args = parser.parse_args()

    target = Path(args.scene_pack)
    scene_yaml = target if target.name == "scene.yaml" else target / "scene.yaml"
    if not scene_yaml.exists():
        fail(f"Missing scene.yaml: {scene_yaml}")

    data = yaml.safe_load(scene_yaml.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("scene.yaml must contain a mapping")

    missing = REQUIRED_TOP - set(data)
    if missing:
        fail(f"Missing required top-level fields: {', '.join(sorted(missing))}")

    fmt = data["format"]
    if not isinstance(fmt, dict) or fmt.get("width") != 1920 or fmt.get("height") != 1080:
        fail("format must be width: 1920 and height: 1080 for this workflow")

    base = scene_yaml.parent
    checked = []
    for section in ("backgrounds", "layers"):
        for rel in iter_paths(data.get(section, {})):
            path = base / rel
            checked.append(rel)
            if path.is_absolute():
                fail(f"Absolute paths are not allowed: {rel}")
            if not path.exists():
                fail(f"Missing asset referenced by {section}: {rel}")

    for prop_id, prop in data.get("props", {}).items():
        variants = prop.get("variants") if isinstance(prop, dict) else None
        if not variants:
            fail(f"Prop '{prop_id}' must define variants")
        for rel in variants.values():
            path = base / rel
            checked.append(rel)
            if Path(rel).is_absolute():
                fail(f"Absolute prop path is not allowed: {rel}")
            if not path.exists():
                fail(f"Missing prop asset for '{prop_id}': {rel}")

    for anchor_id, anchor in data.get("anchors", {}).items():
        if not isinstance(anchor, dict):
            fail(f"Anchor '{anchor_id}' must be a mapping")
        for key in ("x", "y", "scale"):
            if key not in anchor:
                fail(f"Anchor '{anchor_id}' missing {key}")
        if not 0 <= float(anchor["x"]) <= 1:
            fail(f"Anchor '{anchor_id}' x must be normalized")
        if not 0 <= float(anchor["y"]) <= 1:
            fail(f"Anchor '{anchor_id}' y must be normalized")
        if float(anchor["scale"]) <= 0:
            fail(f"Anchor '{anchor_id}' scale must be positive")

    actions = data.get("supported_actions", [])
    if not isinstance(actions, list) or not actions:
        fail("supported_actions must be a non-empty list")

    previews = base / "previews"
    if not previews.exists() or not list(previews.glob("*.png")):
        fail("At least one PNG preview is required in previews/")

    print(f"OK: {data['scene_id']} is valid")
    print(f"Checked {len(set(checked))} referenced assets and {len(data['anchors'])} anchors")


if __name__ == "__main__":
    main()
