import argparse
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


def load_font(size: int):
    for name in ("msyh.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def open_layer(base: Path, rel: str, size: tuple[int, int]) -> Image.Image:
    img = Image.open(base / rel).convert("RGBA")
    if img.size != size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return img


def paste_center(canvas: Image.Image, asset: Image.Image, x: int, y: int, scale: float) -> None:
    w = max(1, int(asset.width * scale))
    h = max(1, int(asset.height * scale))
    img = asset.resize((w, h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(img, (int(x - w / 2), int(y - h / 2)))


def draw_actor(draw: ImageDraw.ImageDraw, anchor: dict, label: str, color: str, width: int, height: int, font) -> None:
    x = int(anchor["x"] * width)
    y = int(anchor["y"] * height)
    scale = float(anchor.get("scale", 1))
    body_w = int(150 * scale)
    body_h = int(390 * scale)
    left = x - body_w // 2
    top = y - body_h
    draw.rounded_rectangle((left, top, left + body_w, y), radius=18, fill=color, outline=(20, 20, 20), width=5)
    draw.ellipse((x - 42, top - 64, x + 42, top + 20), fill=(255, 235, 190), outline=(20, 20, 20), width=5)
    draw.text((left, y + 10), label, fill=(255, 255, 255), font=font, stroke_width=3, stroke_fill=(0, 0, 0))


def render_preview(scene_pack: Path, name: str) -> Path:
    data = yaml.safe_load((scene_pack / "scene.yaml").read_text(encoding="utf-8"))
    size = (int(data["format"]["width"]), int(data["format"]["height"]))
    bg_key = "wide" if "wide" in data["backgrounds"] else next(iter(data["backgrounds"]))
    canvas = open_layer(scene_pack, data["backgrounds"][bg_key], size)

    for rel in data.get("layers", {}).get("behind_character", []):
        canvas.alpha_composite(open_layer(scene_pack, rel, size))

    draw = ImageDraw.Draw(canvas)
    font = load_font(34)
    small_font = load_font(26)

    anchors = data["anchors"]
    if name in ("wide", "all"):
        for anchor_id, anchor in anchors.items():
            x = int(anchor["x"] * size[0])
            y = int(anchor["y"] * size[1])
            draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 80, 40), outline=(0, 0, 0), width=3)
            draw.text((x + 12, y - 22), anchor_id, fill=(255, 240, 210), font=small_font, stroke_width=3, stroke_fill=(0, 0, 0))

    if name in ("sit", "all"):
        if "sit_chair_1" in anchors:
            draw_actor(draw, anchors["sit_chair_1"], "actor@sit_chair_1", (230, 120, 80), *size, font)

    if name in ("pick_phone", "all"):
        if "stand_left" in anchors:
            draw_actor(draw, anchors["stand_left"], "actor@stand_left", (90, 150, 230), *size, font)
        phone = data["props"].get("phone", {}).get("variants", {}).get("table")
        desk_anchor = anchors.get("desk_phone")
        if phone and desk_anchor:
            asset = Image.open(scene_pack / phone).convert("RGBA")
            paste_center(canvas, asset, int(desk_anchor["x"] * size[0]), int(desk_anchor["y"] * size[1]), float(desk_anchor.get("scale", 1)))

    for rel in data.get("layers", {}).get("front_character", []):
        canvas.alpha_composite(open_layer(scene_pack, rel, size))

    previews = scene_pack / "previews"
    previews.mkdir(parents=True, exist_ok=True)
    out = previews / f"preview_{name}.png"
    canvas.convert("RGB").save(out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scene_pack")
    parser.add_argument("--preview", default="all", choices=["wide", "sit", "pick_phone", "all"])
    args = parser.parse_args()

    scene_pack = Path(args.scene_pack)
    names = ["wide", "sit", "pick_phone"] if args.preview == "all" else [args.preview]
    for name in names:
        print(render_preview(scene_pack, name))


if __name__ == "__main__":
    main()
