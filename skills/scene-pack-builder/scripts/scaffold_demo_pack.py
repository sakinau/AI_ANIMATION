import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


def font(size: int):
    for name in ("msyh.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def transparent(size=(1920, 1080)) -> Image.Image:
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save_layer(path: Path, draw_fn) -> None:
    img = transparent()
    draw = ImageDraw.Draw(img)
    draw_fn(draw)
    img.save(path)


def rounded_prop(path: Path, size: tuple[int, int], fill, outline, text: str) -> None:
    img = transparent(size)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((5, 5, size[0] - 5, size[1] - 5), radius=18, fill=fill, outline=outline, width=5)
    draw.text((size[0] * 0.18, size[1] * 0.30), text, fill=(20, 20, 20), font=font(max(18, int(size[1] * 0.28))))
    img.save(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="Directory where scene_demo_school_01 will be created")
    parser.add_argument("--asset-root", default="public/免费素材库", help="Existing free asset library root")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.output_dir) / "scene_demo_school_01"
    if root.exists() and args.overwrite:
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    for sub in ("backgrounds", "layers", "props", "masks", "previews"):
        (root / sub).mkdir(exist_ok=True)

    asset_root = Path(args.asset_root)
    source_bg = asset_root / "背景" / "旧学校.png"
    if not source_bg.exists():
        raise SystemExit(f"Missing source background: {source_bg}")

    wide = root / "backgrounds" / "wide.png"
    shutil.copyfile(source_bg, wide)

    bg = Image.open(source_bg).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    bg.crop((260, 80, 1660, 868)).resize((1920, 1080), Image.Resampling.LANCZOS).save(root / "backgrounds" / "medium.png")
    bg.crop((520, 360, 1400, 900)).resize((1920, 1080), Image.Resampling.LANCZOS).save(root / "backgrounds" / "close_desk.png")

    save_layer(root / "layers" / "desk_back.png", lambda d: d.rounded_rectangle((690, 520, 1245, 620), radius=18, fill=(104, 75, 52, 210), outline=(36, 24, 16, 255), width=5))
    save_layer(root / "layers" / "desk_front.png", lambda d: d.rounded_rectangle((650, 610, 1290, 845), radius=20, fill=(82, 55, 38, 235), outline=(32, 22, 15, 255), width=6))
    save_layer(root / "layers" / "chair_back.png", lambda d: d.rounded_rectangle((755, 500, 920, 710), radius=20, fill=(72, 88, 110, 190), outline=(25, 30, 40, 255), width=5))
    save_layer(root / "layers" / "chair_front.png", lambda d: d.rounded_rectangle((735, 720, 945, 930), radius=18, fill=(54, 66, 86, 235), outline=(20, 24, 34, 255), width=5))
    save_layer(root / "layers" / "door_frame_front.png", lambda d: d.rectangle((1510, 345, 1600, 850), fill=(40, 32, 28, 190), outline=(15, 12, 10, 255), width=5))

    rounded_prop(root / "props" / "phone_table.png", (120, 72), (45, 55, 68, 255), (12, 16, 22, 255), "手机")
    rounded_prop(root / "props" / "phone_hand.png", (92, 60), (45, 55, 68, 255), (12, 16, 22, 255), "机")
    rounded_prop(root / "props" / "book_closed.png", (170, 95), (245, 220, 132, 255), (88, 68, 22, 255), "书")
    rounded_prop(root / "props" / "book_open.png", (220, 110), (250, 242, 214, 255), (100, 80, 40, 255), "打开")
    rounded_prop(root / "props" / "cup_table.png", (82, 92), (245, 245, 245, 255), (44, 44, 44, 255), "杯")
    rounded_prop(root / "props" / "cup_hand.png", (70, 76), (245, 245, 245, 255), (44, 44, 44, 255), "杯")

    scene = {
        "scene_id": "scene_demo_school_01",
        "name": "学校走廊交互样板",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_desk": "backgrounds/close_desk.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": ["layers/chair_back.png", "layers/desk_back.png"],
            "front_character": ["layers/chair_front.png", "layers/desk_front.png", "layers/door_frame_front.png"],
            "overlay": [],
        },
        "anchors": {
            "stand_left": {"x": 0.28, "y": 0.82, "scale": 0.86, "facing": "right"},
            "stand_right": {"x": 0.66, "y": 0.82, "scale": 0.84, "facing": "left"},
            "sit_chair_1": {"x": 0.44, "y": 0.79, "scale": 0.82, "facing": "right"},
            "desk_center": {"x": 0.51, "y": 0.61, "scale": 1.0},
            "desk_phone": {"x": 0.58, "y": 0.55, "scale": 1.0},
            "desk_book": {"x": 0.47, "y": 0.56, "scale": 1.0},
            "desk_cup": {"x": 0.64, "y": 0.56, "scale": 1.0},
            "door_entry": {"x": 0.83, "y": 0.82, "scale": 0.78, "facing": "left"},
            "door_handle": {"x": 0.80, "y": 0.52, "scale": 1.0},
        },
        "props": {
            "phone": {
                "label": "手机",
                "variants": {"table": "props/phone_table.png", "hand": "props/phone_hand.png"},
                "default_anchor": "desk_phone",
                "pivot": "center",
            },
            "book": {
                "label": "书",
                "variants": {"closed": "props/book_closed.png", "open": "props/book_open.png"},
                "default_anchor": "desk_book",
                "pivot": "center",
            },
            "cup": {
                "label": "杯子",
                "variants": {"table": "props/cup_table.png", "hand": "props/cup_hand.png"},
                "default_anchor": "desk_cup",
                "pivot": "center",
            },
        },
        "supported_actions": ["stand", "sit", "pick_up", "put_down", "hand_over", "enter_from_door", "inspect_close"],
        "action_templates": {
            "sit": {
                "duration": 1.0,
                "actor_state_sequence": ["stand", "bend", "sit"],
                "target_anchor": "sit_chair_1",
                "requires_front_layers": ["chair_front"],
            },
            "pick_up": {
                "duration": 1.2,
                "actor_state_sequence": ["reach", "grab", "hold"],
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "desk_phone"},
                    {"time": 0.7, "variant": "hand", "anchor": "actor.hand_r"},
                ],
            },
            "enter_from_door": {
                "duration": 1.4,
                "actor_state_sequence": ["offscreen", "walk", "stand"],
                "from_anchor": "door_entry",
                "requires_front_layers": ["door_frame_front"],
            },
        },
    }
    (root / "scene.yaml").write_text(yaml.safe_dump(scene, allow_unicode=True, sort_keys=False), encoding="utf-8")

    build_preview = Path(__file__).with_name("build_preview.py")
    subprocess.run([sys.executable, str(build_preview), str(root), "--preview", "all"], check=True)
    print(root)


if __name__ == "__main__":
    main()
