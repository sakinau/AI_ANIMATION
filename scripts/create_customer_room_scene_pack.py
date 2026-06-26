from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_customer_room_01")
BACKGROUNDS = ROOT / "backgrounds"
LAYERS = ROOT / "layers"
PROPS = ROOT / "props"
PREVIEWS = ROOT / "previews"
SIZE = (1920, 1080)


def rgba(size=SIZE, color=(0, 0, 0, 0)) -> Image.Image:
    return Image.new("RGBA", size, color)


def font(size: int):
    for name in ("msyh.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def paste_center(canvas: Image.Image, path: Path, anchor: dict, scale: float = 1.0) -> None:
    img = Image.open(path).convert("RGBA")
    final = scale * float(anchor.get("scale", 1.0))
    w = max(1, int(img.width * final))
    h = max(1, int(img.height * final))
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(img, (int(anchor["x"] * SIZE[0] - w / 2), int(anchor["y"] * SIZE[1] - h / 2)))


def draw_actor(draw: ImageDraw.ImageDraw, anchor: dict, label: str, color: tuple[int, int, int, int], fnt) -> None:
    x = int(anchor["x"] * SIZE[0])
    y = int(anchor["y"] * SIZE[1])
    scale = float(anchor.get("scale", 1.0))
    body_w = int(145 * scale)
    body_h = int(365 * scale)
    top = y - body_h
    left = x - body_w // 2
    draw.rounded_rectangle((left, top, left + body_w, y), radius=20, fill=color, outline=(18, 18, 20, 255), width=6)
    draw.ellipse((x - 45, top - 66, x + 45, top + 24), fill=(255, 224, 184, 255), outline=(18, 18, 20, 255), width=6)
    draw.text((left - 8, y + 8), label, fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def draw_room_background(path: Path) -> None:
    img = rgba(color=(224, 214, 202, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(220, 210, 198, 255))
    d.rectangle((0, 0, 1920, 720), fill=(232, 220, 204, 255))
    d.rectangle((0, 720, 1920, 1080), fill=(128, 102, 82, 255))
    for y in range(770, 1080, 92):
        d.line((0, y, 1920, y), fill=(98, 76, 62, 255), width=5)
    for x in range(-160, 2100, 235):
        d.line((x, 720, x + 180, 1080), fill=(100, 78, 64, 255), width=5)

    # Door, window, TV, sofa, table.
    d.rounded_rectangle((92, 260, 405, 805), radius=12, fill=(96, 70, 54, 255), outline=(32, 28, 24, 255), width=8)
    d.rectangle((132, 318, 365, 545), fill=(116, 85, 62, 255), outline=(54, 40, 32, 255), width=5)
    d.rectangle((132, 580, 365, 765), fill=(116, 85, 62, 255), outline=(54, 40, 32, 255), width=5)
    d.ellipse((348, 540, 382, 574), fill=(232, 190, 84, 255), outline=(32, 28, 24, 255), width=4)

    d.rounded_rectangle((1315, 145, 1760, 475), radius=18, fill=(154, 196, 218, 255), outline=(35, 42, 48, 255), width=8)
    d.line((1538, 145, 1538, 475), fill=(35, 42, 48, 255), width=7)
    d.line((1315, 310, 1760, 310), fill=(35, 42, 48, 255), width=7)
    d.polygon([(1324, 466), (1752, 466), (1670, 720), (1405, 720)], fill=(214, 184, 106, 135))

    d.rounded_rectangle((710, 230, 1198, 515), radius=18, fill=(48, 55, 62, 255), outline=(26, 28, 30, 255), width=8)
    d.rectangle((760, 278, 1148, 462), fill=(30, 36, 44, 255))
    d.rectangle((875, 515, 1030, 555), fill=(52, 52, 54, 255), outline=(26, 28, 30, 255), width=5)

    d.rounded_rectangle((725, 648, 1385, 895), radius=38, fill=(86, 126, 158, 255), outline=(34, 44, 54, 255), width=8)
    d.rounded_rectangle((770, 580, 1340, 735), radius=34, fill=(96, 146, 180, 255), outline=(34, 44, 54, 255), width=8)
    d.rounded_rectangle((660, 670, 820, 910), radius=28, fill=(78, 118, 150, 255), outline=(34, 44, 54, 255), width=7)
    d.rounded_rectangle((1290, 670, 1450, 910), radius=28, fill=(78, 118, 150, 255), outline=(34, 44, 54, 255), width=7)

    d.rounded_rectangle((740, 795, 1180, 945), radius=22, fill=(152, 96, 58, 255), outline=(42, 30, 24, 255), width=7)
    d.rectangle((780, 932, 835, 1040), fill=(102, 66, 48, 255), outline=(42, 30, 24, 255), width=5)
    d.rectangle((1085, 932, 1140, 1040), fill=(102, 66, 48, 255), outline=(42, 30, 24, 255), width=5)

    d.rounded_rectangle((1530, 760, 1788, 940), radius=18, fill=(124, 85, 58, 255), outline=(42, 30, 24, 255), width=7)
    d.rectangle((1560, 690, 1758, 770), fill=(166, 112, 70, 255), outline=(42, 30, 24, 255), width=6)
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS).save(target)


def save_layer_table(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((740, 850, 1180, 945), radius=18, fill=(152, 96, 58, 255), outline=(42, 30, 24, 255), width=7)
    d.rectangle((780, 932, 835, 1040), fill=(102, 66, 48, 255), outline=(42, 30, 24, 255), width=5)
    d.rectangle((1085, 932, 1140, 1040), fill=(102, 66, 48, 255), outline=(42, 30, 24, 255), width=5)
    img.save(path)


def save_layer_sofa(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((660, 828, 1450, 918), radius=30, fill=(76, 116, 148, 255), outline=(34, 44, 54, 255), width=7)
    d.rounded_rectangle((660, 670, 820, 910), radius=28, fill=(78, 118, 150, 255), outline=(34, 44, 54, 255), width=7)
    d.rounded_rectangle((1290, 670, 1450, 910), radius=28, fill=(78, 118, 150, 255), outline=(34, 44, 54, 255), width=7)
    img.save(path)


def save_layer_door(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((92, 260, 405, 805), radius=12, outline=(32, 28, 24, 255), width=18)
    img.save(path)


def save_meal_bag(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((520, 460) if close else (280, 260))
    d = ImageDraw.Draw(img)
    s = img.width / 280
    d.rounded_rectangle((45 * s, 82 * s, 238 * s, 235 * s), radius=int(18 * s), fill=(245, 145, 48, 255), outline=(26, 24, 22, 255), width=max(4, int(6 * s)))
    d.polygon([(45 * s, 82 * s), (92 * s, 34 * s), (208 * s, 34 * s), (238 * s, 82 * s)], fill=(255, 184, 70, 255), outline=(26, 24, 22, 255))
    d.rounded_rectangle((92 * s, 122 * s, 198 * s, 174 * s), radius=int(12 * s), fill=(255, 244, 214, 255), outline=(26, 24, 22, 255), width=max(3, int(4 * s)))
    if hand:
        d.rounded_rectangle((180 * s, 24 * s, 278 * s, 88 * s), radius=int(22 * s), fill=(255, 220, 178, 255), outline=(26, 24, 22, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_food_box(path: Path, open_box: bool = False, close: bool = False) -> None:
    img = rgba((580, 420) if close else (300, 220))
    d = ImageDraw.Draw(img)
    s = img.width / 300
    d.rounded_rectangle((42 * s, 90 * s, 258 * s, 190 * s), radius=int(18 * s), fill=(248, 236, 202, 255), outline=(30, 26, 24, 255), width=max(4, int(6 * s)))
    if open_box:
        d.polygon([(54 * s, 88 * s), (130 * s, 34 * s), (248 * s, 84 * s)], fill=(255, 246, 220, 255), outline=(30, 26, 24, 255))
        d.ellipse((92 * s, 112 * s, 168 * s, 164 * s), fill=(235, 108, 62, 255))
        d.rectangle((178 * s, 116 * s, 224 * s, 160 * s), fill=(95, 164, 90, 255))
    else:
        d.rounded_rectangle((82 * s, 118 * s, 218 * s, 150 * s), radius=int(8 * s), fill=(230, 120, 62, 255))
    img.save(path)


def save_phone(path: Path, close: bool = False) -> None:
    img = rgba((520, 740) if close else (220, 310))
    d = ImageDraw.Draw(img)
    s = img.width / 220
    d.rounded_rectangle((38 * s, 12 * s, 182 * s, 292 * s), radius=int(24 * s), fill=(34, 38, 46, 255), outline=(16, 16, 20, 255), width=max(4, int(5 * s)))
    d.rounded_rectangle((54 * s, 42 * s, 166 * s, 250 * s), radius=int(10 * s), fill=(18, 28, 34, 255), outline=(82, 94, 110, 255), width=max(2, int(3 * s)))
    d.rectangle((68 * s, 64 * s, 152 * s, 96 * s), fill=(96, 190, 104, 255))
    for y, w in ((122, 72), (156, 92), (190, 58)):
        d.rectangle((68 * s, y * s, (68 + w) * s, (y + 12) * s), fill=(238, 244, 250, 255))
    img.save(path)


def save_tv_popup(path: Path) -> None:
    img = rgba((640, 360))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 622, 342), radius=24, fill=(38, 48, 58, 245), outline=(240, 210, 90, 255), width=7)
    d.polygon([(82, 70), (142, 198), (22, 198)], fill=(255, 204, 70, 255), outline=(24, 24, 24, 255), width=5)
    d.rectangle((78, 110, 88, 166), fill=(24, 24, 24, 255))
    d.ellipse((72, 176, 94, 198), fill=(24, 24, 24, 255))
    for y, w in ((84, 330), (138, 410), (196, 260)):
        d.rounded_rectangle((188, y, 188 + w, y + 24), radius=8, fill=(248, 240, 210, 255))
    img.save(path)


def save_remote(path: Path, hand: bool = False) -> None:
    img = rgba((180, 330))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((48, 22, 132, 300), radius=22, fill=(42, 46, 52, 255), outline=(18, 18, 20, 255), width=5)
    for y, c in ((58, (230, 80, 70, 255)), (100, (210, 210, 210, 255)), (140, (210, 210, 210, 255)), (180, (210, 210, 210, 255))):
        d.ellipse((74, y, 106, y + 32), fill=c, outline=(18, 18, 20, 255), width=3)
    if hand:
        d.rounded_rectangle((102, 14, 178, 84), radius=20, fill=(255, 220, 178, 255), outline=(18, 18, 20, 255), width=5)
    img.save(path)


def save_key(path: Path, hand: bool = False) -> None:
    img = rgba((240, 160))
    d = ImageDraw.Draw(img)
    d.ellipse((26, 42, 102, 118), fill=(236, 198, 78, 255), outline=(24, 24, 24, 255), width=5)
    d.ellipse((48, 64, 80, 96), fill=(255, 245, 190, 255), outline=(24, 24, 24, 255), width=3)
    d.rectangle((96, 73, 200, 88), fill=(236, 198, 78, 255), outline=(24, 24, 24, 255), width=4)
    d.rectangle((170, 86, 188, 118), fill=(236, 198, 78, 255), outline=(24, 24, 24, 255), width=3)
    if hand:
        d.rounded_rectangle((126, 14, 236, 78), radius=22, fill=(255, 220, 178, 255), outline=(24, 24, 24, 255), width=5)
    img.save(path)


def save_package(path: Path, open_box: bool = False) -> None:
    img = rgba((330, 260))
    d = ImageDraw.Draw(img)
    d.rectangle((44, 82, 286, 230), fill=(176, 116, 72, 255), outline=(42, 30, 24, 255), width=6)
    d.line((165, 82, 165, 230), fill=(130, 82, 56, 255), width=5)
    d.rectangle((68, 112, 138, 146), fill=(240, 220, 170, 255), outline=(42, 30, 24, 255), width=3)
    if open_box:
        d.polygon([(44, 82), (104, 28), (165, 82)], fill=(198, 138, 86, 255), outline=(42, 30, 24, 255))
        d.polygon([(286, 82), (226, 28), (165, 82)], fill=(198, 138, 86, 255), outline=(42, 30, 24, 255))
    img.save(path)


def save_curtain(path: Path) -> None:
    img = rgba((360, 560))
    d = ImageDraw.Draw(img)
    d.polygon([(18, 20), (148, 20), (118, 535), (34, 535)], fill=(210, 94, 92, 210), outline=(86, 48, 48, 255))
    d.polygon([(210, 20), (342, 20), (326, 535), (238, 535)], fill=(210, 94, 92, 210), outline=(86, 48, 48, 255))
    img.save(path)


def save_contact_sheet(path: Path, assets: list[tuple[str, Path]]) -> None:
    thumb = (180, 150)
    margin = 24
    label_h = 30
    cols = 4
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb[0] + margin) + margin, rows * (thumb[1] + label_h + margin) + margin), (232, 228, 220))
    d = ImageDraw.Draw(sheet)
    fnt = font(15)
    for i, (label, asset_path) in enumerate(assets):
        x = margin + (i % cols) * (thumb[0] + margin)
        y = margin + (i // cols) * (thumb[1] + label_h + margin)
        checker = Image.new("RGB", thumb, (250, 250, 250))
        cd = ImageDraw.Draw(checker)
        for yy in range(0, thumb[1], 16):
            for xx in range((yy // 16) % 2 * 16, thumb[0], 32):
                cd.rectangle((xx, yy, xx + 15, yy + 15), fill=(220, 220, 220))
        sheet.paste(checker, (x, y))
        img = Image.open(asset_path).convert("RGBA")
        img.thumbnail(thumb, Image.Resampling.LANCZOS)
        sheet.paste(img, (x + (thumb[0] - img.width) // 2, y + (thumb[1] - img.height) // 2), img)
        d.rectangle((x, y, x + thumb[0], y + thumb[1]), outline=(70, 70, 70), width=2)
        d.text((x, y + thumb[1] + 8), label, fill=(20, 20, 20), font=fnt)
    sheet.save(path)


def scene_yaml() -> dict:
    return {
        "scene_id": "scene_customer_room_01",
        "name": "customer living room interaction pack",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_door": "backgrounds/close_door.png",
            "close_table": "backgrounds/close_table.png",
            "close_tv": "backgrounds/close_tv.png",
            "close_window": "backgrounds/close_window.png",
            "close_package": "backgrounds/close_package.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": ["layers/coffee_table_front.png", "layers/sofa_front.png", "layers/door_frame_front.png"],
            "overlay": [],
        },
        "anchors": {
            "door_entry": {"x": 0.14, "y": 0.82, "scale": 0.82, "facing": "right"},
            "stand_left": {"x": 0.32, "y": 0.84, "scale": 0.86, "facing": "right"},
            "stand_right": {"x": 0.72, "y": 0.84, "scale": 0.86, "facing": "left"},
            "sofa_sit_left": {"x": 0.45, "y": 0.82, "scale": 0.78, "facing": "front"},
            "sofa_sit_right": {"x": 0.62, "y": 0.82, "scale": 0.78, "facing": "front"},
            "table_center": {"x": 0.50, "y": 0.76, "scale": 1.0},
            "table_food": {"x": 0.46, "y": 0.75, "scale": 1.0},
            "table_phone": {"x": 0.57, "y": 0.74, "scale": 1.0},
            "table_remote": {"x": 0.64, "y": 0.76, "scale": 1.0},
            "door_handle": {"x": 0.19, "y": 0.52, "scale": 1.0},
            "handoff_mid": {"x": 0.28, "y": 0.58, "scale": 1.0},
            "tv_center": {"x": 0.50, "y": 0.36, "scale": 1.0},
            "window_center": {"x": 0.80, "y": 0.30, "scale": 1.0},
            "package_corner": {"x": 0.86, "y": 0.78, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
        },
        "props": {
            "meal_bag": {
                "label": "meal delivery bag",
                "variants": {"floor": "props/meal_bag_floor.png", "hand": "props/meal_bag_hand.png", "close": "props/meal_bag_close.png"},
                "default_anchor": "handoff_mid",
                "pivot": "center",
                "variant_scales": {"floor": 0.78, "hand": 0.58, "close": 1.0},
            },
            "food_box": {
                "label": "food box",
                "variants": {"closed": "props/food_box_closed.png", "open": "props/food_box_open.png", "close": "props/food_box_close.png"},
                "default_anchor": "table_food",
                "pivot": "center",
                "variant_scales": {"closed": 0.72, "open": 0.74, "close": 1.0},
            },
            "phone": {
                "label": "confirmation phone",
                "variants": {"table": "props/phone_table.png", "close": "props/phone_close.png"},
                "default_anchor": "table_phone",
                "pivot": "center",
                "variant_scales": {"table": 0.58, "close": 0.95},
            },
            "tv_popup": {
                "label": "TV popup",
                "variants": {"warning": "props/tv_popup_warning.png"},
                "default_anchor": "tv_center",
                "pivot": "center",
                "variant_scales": {"warning": 0.78},
            },
            "remote": {
                "label": "remote control",
                "variants": {"table": "props/remote_table.png", "hand": "props/remote_hand.png"},
                "default_anchor": "table_remote",
                "pivot": "center",
                "variant_scales": {"table": 0.5, "hand": 0.48},
            },
            "key": {
                "label": "door key",
                "variants": {"table": "props/key_table.png", "hand": "props/key_hand.png"},
                "default_anchor": "door_handle",
                "pivot": "center",
                "variant_scales": {"table": 0.56, "hand": 0.52},
            },
            "package": {
                "label": "corner package",
                "variants": {"closed": "props/package_closed.png", "open": "props/package_open.png"},
                "default_anchor": "package_corner",
                "pivot": "center",
                "variant_scales": {"closed": 0.82, "open": 0.82},
            },
            "curtain": {
                "label": "window curtain",
                "variants": {"open": "props/curtain_open.png"},
                "default_anchor": "window_center",
                "pivot": "center",
                "variant_scales": {"open": 1.0},
            },
        },
        "supported_actions": [
            "stand",
            "enter_room",
            "door_handoff",
            "place_meal_on_table",
            "open_food_box",
            "confirm_delivery",
            "sit_sofa",
            "watch_tv_warning",
            "pick_remote",
            "unlock_door",
            "open_package",
            "inspect_window",
            "inspect_close",
        ],
        "action_templates": {
            "enter_room": {"duration": 1.0, "actor_state_sequence": ["offscreen", "step_in", "stand"], "from_anchor": "door_entry"},
            "door_handoff": {
                "duration": 1.2,
                "prop": "meal_bag",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "actor.hand_r"},
                    {"time": 0.7, "variant": "hand", "anchor": "handoff_mid"},
                ],
            },
            "place_meal_on_table": {
                "duration": 1.2,
                "prop": "food_box",
                "prop_sequence": [
                    {"time": 0.0, "variant": "closed", "anchor": "actor.hand_r"},
                    {"time": 0.65, "variant": "closed", "anchor": "table_food"},
                ],
            },
            "open_food_box": {
                "duration": 1.0,
                "prop": "food_box",
                "prop_sequence": [
                    {"time": 0.0, "variant": "closed", "anchor": "table_food"},
                    {"time": 0.55, "variant": "open", "anchor": "table_food"},
                    {"time": 0.8, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "confirm_delivery": {
                "duration": 1.1,
                "prop": "phone",
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "table_phone"},
                    {"time": 0.6, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "sit_sofa": {"duration": 1.0, "actor_state_sequence": ["stand", "turn", "sit"], "target_anchor": "sofa_sit_left"},
            "watch_tv_warning": {
                "duration": 1.0,
                "prop": "tv_popup",
                "prop_sequence": [{"time": 0.0, "variant": "warning", "anchor": "tv_center", "motion": "pop_in"}],
            },
            "pick_remote": {
                "duration": 0.9,
                "prop": "remote",
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "table_remote"},
                    {"time": 0.55, "variant": "hand", "anchor": "actor.hand_r"},
                ],
            },
            "unlock_door": {
                "duration": 0.9,
                "prop": "key",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "actor.hand_r"},
                    {"time": 0.55, "variant": "table", "anchor": "door_handle"},
                ],
            },
            "open_package": {
                "duration": 1.0,
                "prop": "package",
                "prop_sequence": [
                    {"time": 0.0, "variant": "closed", "anchor": "package_corner"},
                    {"time": 0.6, "variant": "open", "anchor": "package_corner"},
                ],
            },
            "inspect_window": {
                "duration": 1.0,
                "background": "close_window",
                "prop": "curtain",
                "prop_sequence": [{"time": 0.0, "variant": "open", "anchor": "close_insert_center"}],
            },
        },
    }


def render_base(data: dict, bg_key: str = "wide", front_layers: bool = True) -> Image.Image:
    canvas = Image.open(ROOT / data["backgrounds"][bg_key]).convert("RGBA")
    if front_layers:
        for rel in data["layers"]["front_character"]:
            canvas.alpha_composite(Image.open(ROOT / rel).convert("RGBA"))
    return canvas


def render_previews(data: dict) -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    fnt = font(34)
    small = font(24)
    anchors = data["anchors"]

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    for anchor_id, anchor in anchors.items():
        x = int(anchor["x"] * SIZE[0])
        y = int(anchor["y"] * SIZE[1])
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 90, 50, 255), outline=(0, 0, 0, 255), width=3)
        draw.text((x + 12, y - 22), anchor_id, fill=(255, 244, 190, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    for layer in ("coffee_table_front.png", "sofa_front.png", "door_frame_front.png"):
        canvas.alpha_composite(Image.open(LAYERS / layer).convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "food_box_closed.png", anchors["table_food"], 0.72)
    paste_center(canvas, PROPS / "phone_table.png", anchors["table_phone"], 0.58)
    paste_center(canvas, PROPS / "remote_table.png", anchors["table_remote"], 0.5)
    paste_center(canvas, PROPS / "package_closed.png", anchors["package_corner"], 0.82)
    paste_center(canvas, PROPS / "meal_bag_floor.png", anchors["handoff_mid"], 0.78)
    canvas.alpha_composite(Image.open(LAYERS / "coffee_table_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "customer room props", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["door_entry"], "courier", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["stand_left"], "customer", (210, 92, 72, 255), fnt)
    paste_center(canvas, PROPS / "meal_bag_hand.png", anchors["handoff_mid"], 0.58)
    canvas.alpha_composite(Image.open(LAYERS / "door_frame_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "door_handoff", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_door_handoff.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["sofa_sit_left"], "customer", (210, 92, 72, 255), fnt)
    paste_center(canvas, PROPS / "food_box_open.png", anchors["table_food"], 0.74)
    paste_center(canvas, PROPS / "phone_table.png", anchors["table_phone"], 0.58)
    canvas.alpha_composite(Image.open(LAYERS / "sofa_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "coffee_table_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "sit_sofa + open_food_box", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_sofa_food.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "tv_popup_warning.png", anchors["tv_center"], 0.78)
    paste_center(canvas, PROPS / "remote_hand.png", anchors["table_remote"], 0.48)
    ImageDraw.Draw(canvas).text((60, 60), "watch_tv_warning + remote", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_tv_warning.png")

    canvas = render_base(data, bg_key="close_table", front_layers=False)
    paste_center(canvas, PROPS / "food_box_close.png", anchors["close_insert_center"], 1.0)
    ImageDraw.Draw(canvas).text((60, 60), "food close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_food_close.png")

    canvas = render_base(data, bg_key="close_tv", front_layers=False)
    paste_center(canvas, PROPS / "tv_popup_warning.png", anchors["close_insert_center"], 0.78)
    ImageDraw.Draw(canvas).text((60, 60), "TV close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_tv_close.png")

    canvas = render_base(data, bg_key="close_package", front_layers=False)
    paste_center(canvas, PROPS / "package_open.png", anchors["close_insert_center"], 0.82)
    ImageDraw.Draw(canvas).text((60, 60), "package close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_package_close.png")

    save_contact_sheet(
        PREVIEWS / "customer_room_props_contact_sheet.png",
        [
            ("meal_bag_floor", PROPS / "meal_bag_floor.png"),
            ("meal_bag_hand", PROPS / "meal_bag_hand.png"),
            ("food_box_closed", PROPS / "food_box_closed.png"),
            ("food_box_open", PROPS / "food_box_open.png"),
            ("phone_table", PROPS / "phone_table.png"),
            ("tv_popup", PROPS / "tv_popup_warning.png"),
            ("remote_table", PROPS / "remote_table.png"),
            ("remote_hand", PROPS / "remote_hand.png"),
            ("key_hand", PROPS / "key_hand.png"),
            ("package_closed", PROPS / "package_closed.png"),
            ("package_open", PROPS / "package_open.png"),
            ("curtain_open", PROPS / "curtain_open.png"),
        ],
    )


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)

    draw_room_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (380, 210, 1540, 930))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_door.png", (40, 220, 470, 850))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_table.png", (650, 690, 1240, 980))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_tv.png", (650, 165, 1260, 570))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_window.png", (1240, 90, 1825, 520))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_package.png", (1460, 650, 1850, 980))

    save_layer_table(LAYERS / "coffee_table_front.png")
    save_layer_sofa(LAYERS / "sofa_front.png")
    save_layer_door(LAYERS / "door_frame_front.png")

    save_meal_bag(PROPS / "meal_bag_floor.png")
    save_meal_bag(PROPS / "meal_bag_hand.png", hand=True)
    save_meal_bag(PROPS / "meal_bag_close.png", close=True)
    save_food_box(PROPS / "food_box_closed.png")
    save_food_box(PROPS / "food_box_open.png", open_box=True)
    save_food_box(PROPS / "food_box_close.png", open_box=True, close=True)
    save_phone(PROPS / "phone_table.png")
    save_phone(PROPS / "phone_close.png", close=True)
    save_tv_popup(PROPS / "tv_popup_warning.png")
    save_remote(PROPS / "remote_table.png")
    save_remote(PROPS / "remote_hand.png", hand=True)
    save_key(PROPS / "key_table.png")
    save_key(PROPS / "key_hand.png", hand=True)
    save_package(PROPS / "package_closed.png")
    save_package(PROPS / "package_open.png", open_box=True)
    save_curtain(PROPS / "curtain_open.png")

    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
