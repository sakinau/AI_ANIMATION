import argparse
import os
import shutil
import time
from contextlib import contextmanager
from pathlib import Path

import yaml
from PIL import Image


def rel(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def normalize_png(source: Path, target: Path, size: tuple[int, int] | None = None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(source).convert("RGBA")
    if size and img.size != size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    img.save(target)


@contextmanager
def scene_lock(scene_pack: Path, timeout: float = 30.0):
    lock_path = scene_pack / ".scene_yaml.lock"
    deadline = time.time() + timeout
    fd = None
    while time.time() < deadline:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode("utf-8"))
            break
        except FileExistsError:
            time.sleep(0.1)
    if fd is None:
        raise SystemExit(f"Timed out waiting for scene.yaml lock: {lock_path}")
    try:
        yield
    finally:
        os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Register a generated asset into a scene pack and update scene.yaml.")
    parser.add_argument("scene_pack")
    parser.add_argument("source_image")
    parser.add_argument("--kind", required=True, choices=["background", "layer", "prop"])
    parser.add_argument("--key", help="Background key or layer file stem")
    parser.add_argument("--layer-group", choices=["behind_character", "front_character", "overlay"], default="front_character")
    parser.add_argument("--prop")
    parser.add_argument("--variant")
    parser.add_argument("--label")
    parser.add_argument("--default-anchor")
    parser.add_argument("--resize-1080p", action="store_true", help="Resize backgrounds/layers to 1920x1080")
    args = parser.parse_args()

    scene_pack = Path(args.scene_pack)
    source = Path(args.source_image)
    scene_yaml = scene_pack / "scene.yaml"

    with scene_lock(scene_pack):
        data = yaml.safe_load(scene_yaml.read_text(encoding="utf-8"))
        size = (int(data["format"]["width"]), int(data["format"]["height"])) if args.resize_1080p else None

        if args.kind == "background":
            if not args.key:
                raise SystemExit("--key is required for backgrounds")
            target = scene_pack / "backgrounds" / f"{args.key}.png"
            normalize_png(source, target, size)
            data.setdefault("backgrounds", {})[args.key] = rel(target, scene_pack)
            if args.key == "wide":
                bg_layers = data.setdefault("layers", {}).setdefault("background", [])
                if rel(target, scene_pack) not in bg_layers:
                    bg_layers[:] = [rel(target, scene_pack)]

        elif args.kind == "layer":
            if not args.key:
                raise SystemExit("--key is required for layers")
            target = scene_pack / "layers" / f"{args.key}.png"
            normalize_png(source, target, size)
            group = data.setdefault("layers", {}).setdefault(args.layer_group, [])
            path = rel(target, scene_pack)
            if path not in group:
                group.append(path)

        elif args.kind == "prop":
            if not args.prop or not args.variant:
                raise SystemExit("--prop and --variant are required for props")
            target = scene_pack / "props" / f"{args.prop}_{args.variant}.png"
            shutil.copyfile(source, target)
            prop = data.setdefault("props", {}).setdefault(args.prop, {})
            prop.setdefault("label", args.label or args.prop)
            prop.setdefault("variants", {})[args.variant] = rel(target, scene_pack)
            prop.setdefault("pivot", "center")
            if args.default_anchor:
                prop["default_anchor"] = args.default_anchor

        scene_yaml.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
