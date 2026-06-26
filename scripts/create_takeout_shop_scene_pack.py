from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_takeout_shop_01")
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
    x = int(anchor["x"] * SIZE[0] - w / 2)
    y = int(anchor["y"] * SIZE[1] - h / 2)
    canvas.alpha_composite(img, (x, y))


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
    draw.text((left - 10, y + 8), label, fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def draw_shop_background(path: Path) -> None:
    img = rgba(color=(236, 218, 184, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(235, 214, 180, 255))
    d.rectangle((0, 0, 1920, 250), fill=(216, 92, 66, 255))
    d.rectangle((0, 250, 1920, 715), fill=(246, 229, 194, 255))
    d.rectangle((0, 715, 1920, 1080), fill=(96, 82, 70, 255))
    for y in range(775, 1080, 92):
        d.line((0, y, 1920, y), fill=(70, 60, 54, 255), width=5)
    for x in range(-80, 2000, 210):
        d.line((x, 715, x + 160, 1080), fill=(74, 63, 57, 255), width=5)

    # Signboard, menu, pass-through kitchen window.
    d.rounded_rectangle((118, 62, 710, 188), radius=24, fill=(255, 196, 70, 255), outline=(32, 28, 24, 255), width=7)
    d.rectangle((160, 103, 664, 142), fill=(45, 38, 32, 255))
    d.rounded_rectangle((1230, 76, 1788, 222), radius=18, fill=(50, 68, 74, 255), outline=(28, 28, 28, 255), width=7)
    for y in (112, 152, 192):
        d.rectangle((1282, y, 1702, y + 16), fill=(238, 235, 190, 255))
    d.rounded_rectangle((760, 310, 1220, 595), radius=18, fill=(75, 65, 58, 255), outline=(30, 28, 26, 255), width=8)
    d.rectangle((805, 348, 1175, 555), fill=(54, 50, 47, 255))
    for x in (860, 980, 1100):
        d.ellipse((x, 390, x + 50, 455), fill=(250, 178, 72, 255), outline=(30, 28, 26, 255), width=4)
        d.rectangle((x + 20, 454, x + 30, 530), fill=(210, 86, 64, 255))

    # Dining table and shelves.
    d.rounded_rectangle((110, 590, 540, 820), radius=20, fill=(126, 82, 52, 255), outline=(40, 30, 24, 255), width=7)
    d.rectangle((145, 810, 190, 1010), fill=(90, 58, 42, 255), outline=(40, 30, 24, 255), width=5)
    d.rectangle((455, 810, 500, 1010), fill=(90, 58, 42, 255), outline=(40, 30, 24, 255), width=5)
    for x in (103, 468):
        d.rounded_rectangle((x, 820, x + 100, 1000), radius=18, fill=(78, 70, 65, 255), outline=(35, 30, 28, 255), width=5)
    d.rounded_rectangle((1330, 330, 1810, 570), radius=16, fill=(144, 93, 55, 255), outline=(42, 30, 24, 255), width=7)
    for x in range(1375, 1780, 92):
        d.rounded_rectangle((x, 382, x + 52, 524), radius=12, fill=(250, 224, 160, 255), outline=(48, 38, 30, 255), width=4)

    # Main counter.
    d.rounded_rectangle((585, 635, 1548, 910), radius=24, fill=(154, 94, 52, 255), outline=(42, 30, 24, 255), width=8)
    d.rectangle((625, 666, 1508, 742), fill=(184, 120, 64, 255), outline=(42, 30, 24, 255), width=5)
    d.rectangle((690, 748, 925, 870), fill=(108, 68, 48, 255), outline=(42, 30, 24, 255), width=5)
    d.rectangle((1200, 748, 1465, 870), fill=(108, 68, 48, 255), outline=(42, 30, 24, 255), width=5)
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS).save(target)


def save_layer_counter(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((585, 710, 1548, 930), radius=24, fill=(135, 82, 50, 255), outline=(42, 30, 24, 255), width=8)
    d.rectangle((625, 705, 1508, 755), fill=(196, 128, 70, 255), outline=(42, 30, 24, 255), width=6)
    img.save(path)


def save_layer_shelf(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1325, 325, 1815, 575), radius=18, fill=(110, 72, 48, 105), outline=(42, 30, 24, 220), width=6)
    d.rectangle((1325, 442, 1815, 462), fill=(72, 48, 36, 185))
    img.save(path)


def save_layer_door_frame(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((760, 305, 1220, 600), radius=18, outline=(34, 28, 24, 240), width=18)
    img.save(path)


def save_meal_tray(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((640, 420) if close else (330, 230))
    d = ImageDraw.Draw(img)
    s = img.width / 330
    d.rounded_rectangle((42 * s, 112 * s, 290 * s, 205 * s), radius=int(20 * s), fill=(238, 142, 62, 255), outline=(26, 24, 22, 255), width=max(4, int(6 * s)))
    d.ellipse((72 * s, 48 * s, 168 * s, 138 * s), fill=(255, 236, 190, 255), outline=(26, 24, 22, 255), width=max(3, int(5 * s)))
    d.ellipse((92 * s, 68 * s, 148 * s, 118 * s), fill=(235, 106, 58, 255))
    d.rounded_rectangle((184 * s, 56 * s, 262 * s, 142 * s), radius=int(12 * s), fill=(245, 230, 190, 255), outline=(26, 24, 22, 255), width=max(3, int(5 * s)))
    if hand:
        d.rounded_rectangle((238 * s, 22 * s, 328 * s, 88 * s), radius=int(22 * s), fill=(255, 220, 178, 255), outline=(26, 24, 22, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_noodle_bowl(path: Path, close: bool = False) -> None:
    img = rgba((520, 420) if close else (240, 190))
    d = ImageDraw.Draw(img)
    s = img.width / 240
    d.ellipse((32 * s, 52 * s, 210 * s, 132 * s), fill=(255, 242, 198, 255), outline=(28, 24, 22, 255), width=max(3, int(5 * s)))
    for x in (62, 90, 118, 146):
        d.arc((x * s, 66 * s, (x + 62) * s, 118 * s), 180, 350, fill=(230, 164, 62, 255), width=max(2, int(4 * s)))
    d.polygon([(48 * s, 104 * s), (194 * s, 104 * s), (164 * s, 172 * s), (78 * s, 172 * s)], fill=(210, 86, 64, 255), outline=(28, 24, 22, 255))
    d.line((58 * s, 42 * s, 204 * s, 10 * s), fill=(50, 40, 34, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_receipt(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((520, 660) if close else (220, 300))
    d = ImageDraw.Draw(img)
    s = img.width / 220
    d.polygon([(30 * s, 18 * s), (190 * s, 18 * s), (190 * s, 270 * s), (168 * s, 252 * s), (146 * s, 270 * s), (124 * s, 252 * s), (102 * s, 270 * s), (80 * s, 252 * s), (58 * s, 270 * s), (30 * s, 270 * s)], fill=(255, 250, 226, 255), outline=(36, 30, 26, 255))
    for y, w in ((52, 104), (86, 128), (120, 98), (154, 136), (202, 82)):
        d.rectangle((54 * s, y * s, (54 + w) * s, (y + 12) * s), fill=(70, 58, 48, 255))
    if hand:
        d.rounded_rectangle((128 * s, 16 * s, 218 * s, 76 * s), radius=int(18 * s), fill=(255, 220, 178, 255), outline=(26, 24, 22, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_qr_code(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((520, 520) if close else (240, 240))
    d = ImageDraw.Draw(img)
    s = img.width / 240
    d.rounded_rectangle((18 * s, 18 * s, 222 * s, 222 * s), radius=int(16 * s), fill=(255, 255, 248, 255), outline=(28, 26, 24, 255), width=max(4, int(6 * s)))
    for bx, by in ((42, 42), (154, 42), (42, 154)):
        d.rectangle((bx * s, by * s, (bx + 44) * s, (by + 44) * s), fill=(32, 32, 32, 255))
        d.rectangle(((bx + 12) * s, (by + 12) * s, (bx + 32) * s, (by + 32) * s), fill=(255, 255, 248, 255))
    for i, (x, y) in enumerate(((114, 58), (126, 86), (150, 126), (92, 134), (126, 166), (166, 176), (104, 194))):
        d.rectangle((x * s, y * s, (x + 18 + i % 2 * 12) * s, (y + 18) * s), fill=(32, 32, 32, 255))
    if hand:
        d.rounded_rectangle((128 * s, 170 * s, 238 * s, 232 * s), radius=int(20 * s), fill=(255, 220, 178, 255), outline=(26, 24, 22, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_drink(path: Path, hand: bool = False) -> None:
    img = rgba((210, 300))
    d = ImageDraw.Draw(img)
    d.polygon([(56, 70), (162, 70), (148, 260), (70, 260)], fill=(122, 202, 232, 255), outline=(24, 24, 24, 255))
    d.rectangle((46, 50, 172, 82), fill=(245, 245, 238, 255), outline=(24, 24, 24, 255), width=5)
    d.line((138, 20, 112, 96), fill=(36, 32, 30, 255), width=7)
    d.rectangle((82, 136, 138, 172), fill=(255, 244, 214, 255), outline=(24, 24, 24, 255), width=4)
    if hand:
        d.rounded_rectangle((116, 42, 208, 108), radius=22, fill=(255, 220, 178, 255), outline=(24, 24, 24, 255), width=5)
    img.save(path)


def save_delivery_bag(path: Path, hand: bool = False) -> None:
    img = rgba((310, 270))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((44, 82, 260, 238), radius=20, fill=(245, 145, 48, 255), outline=(26, 24, 22, 255), width=6)
    d.polygon([(44, 82), (94, 30), (218, 30), (260, 82)], fill=(255, 184, 70, 255), outline=(26, 24, 22, 255))
    d.rounded_rectangle((94, 120, 204, 174), radius=13, fill=(255, 244, 214, 255), outline=(26, 24, 22, 255), width=4)
    if hand:
        d.rounded_rectangle((190, 24, 304, 92), radius=22, fill=(255, 220, 178, 255), outline=(26, 24, 22, 255), width=5)
    img.save(path)


def save_counter_bell(path: Path) -> None:
    img = rgba((190, 140))
    d = ImageDraw.Draw(img)
    d.ellipse((74, 14, 116, 48), fill=(230, 210, 130, 255), outline=(26, 24, 22, 255), width=5)
    d.pieslice((32, 36, 158, 132), 180, 360, fill=(236, 202, 88, 255), outline=(26, 24, 22, 255), width=6)
    d.rectangle((22, 112, 168, 132), fill=(78, 68, 60, 255), outline=(26, 24, 22, 255), width=4)
    img.save(path)


def save_menu_board(path: Path) -> None:
    img = rgba((600, 360))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, 580, 340), radius=20, fill=(48, 68, 70, 255), outline=(26, 24, 22, 255), width=7)
    for y, w, c in ((70, 390, (244, 238, 178, 255)), (126, 450, (244, 238, 178, 255)), (182, 330, (244, 238, 178, 255)), (250, 210, (255, 198, 74, 255))):
        d.rounded_rectangle((70, y, 70 + w, y + 24), radius=7, fill=c)
    img.save(path)


def save_steam(path: Path) -> None:
    img = rgba((500, 360))
    d = ImageDraw.Draw(img)
    for x in (88, 182, 282, 370):
        d.arc((x, 30, x + 88, 300), 90, 260, fill=(255, 255, 255, 130), width=10)
        d.arc((x - 35, 70, x + 70, 330), 270, 80, fill=(255, 255, 255, 90), width=8)
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
        "scene_id": "scene_takeout_shop_01",
        "name": "takeout shop counter interaction pack",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_counter": "backgrounds/close_counter.png",
            "close_kitchen": "backgrounds/close_kitchen.png",
            "close_menu": "backgrounds/close_menu.png",
            "close_table": "backgrounds/close_table.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": [
                "layers/counter_front.png",
                "layers/shelf_front.png",
                "layers/kitchen_window_frame_front.png",
            ],
            "overlay": [],
        },
        "anchors": {
            "stand_left": {"x": 0.28, "y": 0.84, "scale": 0.86, "facing": "right"},
            "stand_counter": {"x": 0.47, "y": 0.84, "scale": 0.88, "facing": "right"},
            "clerk_counter": {"x": 0.67, "y": 0.78, "scale": 0.78, "facing": "left"},
            "table_sit_left": {"x": 0.18, "y": 0.83, "scale": 0.78, "facing": "right"},
            "table_sit_right": {"x": 0.28, "y": 0.83, "scale": 0.78, "facing": "left"},
            "counter_center": {"x": 0.56, "y": 0.64, "scale": 1.0},
            "counter_meal": {"x": 0.48, "y": 0.61, "scale": 1.0},
            "counter_receipt": {"x": 0.61, "y": 0.59, "scale": 1.0},
            "counter_qr": {"x": 0.72, "y": 0.57, "scale": 1.0},
            "counter_bell": {"x": 0.41, "y": 0.61, "scale": 1.0},
            "bag_floor": {"x": 0.34, "y": 0.80, "scale": 1.0},
            "drink_counter": {"x": 0.78, "y": 0.60, "scale": 1.0},
            "kitchen_window": {"x": 0.51, "y": 0.42, "scale": 1.0},
            "menu_board": {"x": 0.79, "y": 0.16, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "steam_center": {"x": 0.51, "y": 0.38, "scale": 1.0},
        },
        "props": {
            "meal_tray": {
                "label": "meal tray",
                "variants": {
                    "counter": "props/meal_tray_counter.png",
                    "hand": "props/meal_tray_hand.png",
                    "close": "props/meal_tray_close.png",
                },
                "default_anchor": "counter_meal",
                "pivot": "center",
                "variant_scales": {"counter": 0.78, "hand": 0.58, "close": 1.0},
            },
            "noodle_bowl": {
                "label": "noodle bowl",
                "variants": {"table": "props/noodle_bowl_table.png", "close": "props/noodle_bowl_close.png"},
                "default_anchor": "counter_meal",
                "pivot": "center",
                "variant_scales": {"table": 0.76, "close": 1.0},
            },
            "receipt": {
                "label": "receipt",
                "variants": {
                    "counter": "props/receipt_counter.png",
                    "hand": "props/receipt_hand.png",
                    "close": "props/receipt_close.png",
                },
                "default_anchor": "counter_receipt",
                "pivot": "center",
                "variant_scales": {"counter": 0.62, "hand": 0.56, "close": 0.95},
            },
            "qr_code": {
                "label": "qr payment code",
                "variants": {
                    "counter": "props/qr_code_counter.png",
                    "hand": "props/qr_code_hand.png",
                    "close": "props/qr_code_close.png",
                },
                "default_anchor": "counter_qr",
                "pivot": "center",
                "variant_scales": {"counter": 0.58, "hand": 0.54, "close": 0.9},
            },
            "drink": {
                "label": "drink cup",
                "variants": {"counter": "props/drink_counter.png", "hand": "props/drink_hand.png"},
                "default_anchor": "drink_counter",
                "pivot": "center",
                "variant_scales": {"counter": 0.58, "hand": 0.52},
            },
            "delivery_bag": {
                "label": "delivery bag",
                "variants": {"floor": "props/delivery_bag_floor.png", "hand": "props/delivery_bag_hand.png"},
                "default_anchor": "bag_floor",
                "pivot": "center",
                "variant_scales": {"floor": 0.78, "hand": 0.58},
            },
            "counter_bell": {
                "label": "counter bell",
                "variants": {"idle": "props/counter_bell_idle.png"},
                "default_anchor": "counter_bell",
                "pivot": "center",
                "variant_scales": {"idle": 0.72},
            },
            "menu_board": {
                "label": "menu board",
                "variants": {"close": "props/menu_board_close.png"},
                "default_anchor": "menu_board",
                "pivot": "center",
                "variant_scales": {"close": 0.82},
            },
            "steam": {
                "label": "kitchen steam",
                "variants": {"puff": "props/steam_puff.png"},
                "default_anchor": "steam_center",
                "pivot": "center",
                "variant_scales": {"puff": 1.0},
            },
        },
        "supported_actions": [
            "stand",
            "sit_table",
            "ring_bell",
            "pack_meal",
            "pick_up_order",
            "hand_over_meal",
            "scan_payment",
            "read_receipt",
            "inspect_menu",
            "kitchen_steam",
            "drink_pickup",
            "inspect_close",
        ],
        "action_templates": {
            "sit_table": {
                "duration": 1.0,
                "actor_state_sequence": ["stand", "turn", "sit"],
                "target_anchor": "table_sit_left",
            },
            "ring_bell": {
                "duration": 0.8,
                "prop": "counter_bell",
                "prop_sequence": [{"time": 0.0, "variant": "idle", "anchor": "counter_bell", "motion": "tap"}],
            },
            "pack_meal": {
                "duration": 1.4,
                "prop": "meal_tray",
                "prop_sequence": [
                    {"time": 0.0, "variant": "counter", "anchor": "counter_meal"},
                    {"time": 0.75, "variant": "hand", "anchor": "clerk_counter"},
                ],
            },
            "pick_up_order": {
                "duration": 1.2,
                "prop": "delivery_bag",
                "prop_sequence": [
                    {"time": 0.0, "variant": "floor", "anchor": "bag_floor"},
                    {"time": 0.65, "variant": "hand", "anchor": "actor.hand_r"},
                ],
            },
            "hand_over_meal": {
                "duration": 1.2,
                "prop": "meal_tray",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "clerk_counter"},
                    {"time": 0.7, "variant": "hand", "anchor": "actor.hand_l"},
                ],
            },
            "scan_payment": {
                "duration": 1.1,
                "prop": "qr_code",
                "prop_sequence": [
                    {"time": 0.0, "variant": "counter", "anchor": "counter_qr"},
                    {"time": 0.65, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "read_receipt": {
                "duration": 1.1,
                "prop": "receipt",
                "prop_sequence": [
                    {"time": 0.0, "variant": "counter", "anchor": "counter_receipt"},
                    {"time": 0.55, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "inspect_menu": {
                "duration": 1.0,
                "background": "close_menu",
                "prop": "menu_board",
                "prop_sequence": [{"time": 0.0, "variant": "close", "anchor": "close_insert_center"}],
            },
            "kitchen_steam": {
                "duration": 0.8,
                "prop": "steam",
                "prop_sequence": [{"time": 0.0, "variant": "puff", "anchor": "steam_center", "motion": "loop_up"}],
            },
            "drink_pickup": {
                "duration": 0.9,
                "prop": "drink",
                "prop_sequence": [
                    {"time": 0.0, "variant": "counter", "anchor": "drink_counter"},
                    {"time": 0.55, "variant": "hand", "anchor": "actor.hand_r"},
                ],
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
    for layer in ("counter_front.png", "shelf_front.png", "kitchen_window_frame_front.png"):
        canvas.alpha_composite(Image.open(LAYERS / layer).convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "meal_tray_counter.png", anchors["counter_meal"], 0.78)
    paste_center(canvas, PROPS / "receipt_counter.png", anchors["counter_receipt"], 0.62)
    paste_center(canvas, PROPS / "qr_code_counter.png", anchors["counter_qr"], 0.58)
    paste_center(canvas, PROPS / "counter_bell_idle.png", anchors["counter_bell"], 0.72)
    paste_center(canvas, PROPS / "drink_counter.png", anchors["drink_counter"], 0.58)
    paste_center(canvas, PROPS / "delivery_bag_floor.png", anchors["bag_floor"], 0.78)
    canvas.alpha_composite(Image.open(LAYERS / "counter_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "takeout shop props", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_counter"], "courier", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["clerk_counter"], "clerk", (210, 92, 72, 255), fnt)
    paste_center(canvas, PROPS / "meal_tray_hand.png", anchors["counter_center"], 0.58)
    paste_center(canvas, PROPS / "delivery_bag_floor.png", anchors["bag_floor"], 0.78)
    canvas.alpha_composite(Image.open(LAYERS / "counter_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "hand_over_meal + pickup", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_handover.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_counter"], "courier", (80, 145, 230, 255), fnt)
    paste_center(canvas, PROPS / "qr_code_counter.png", anchors["counter_qr"], 0.58)
    paste_center(canvas, PROPS / "receipt_counter.png", anchors["counter_receipt"], 0.62)
    paste_center(canvas, PROPS / "counter_bell_idle.png", anchors["counter_bell"], 0.72)
    canvas.alpha_composite(Image.open(LAYERS / "counter_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "scan_payment + receipt", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_scan_receipt.png")

    canvas = render_base(data, bg_key="close_kitchen", front_layers=False)
    paste_center(canvas, PROPS / "steam_puff.png", anchors["steam_center"], 1.0)
    paste_center(canvas, PROPS / "noodle_bowl_close.png", anchors["close_insert_center"], 0.72)
    ImageDraw.Draw(canvas).text((60, 60), "kitchen steam / food insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_kitchen_steam.png")

    canvas = render_base(data, bg_key="close_counter", front_layers=False)
    paste_center(canvas, PROPS / "meal_tray_close.png", anchors["close_insert_center"], 1.0)
    ImageDraw.Draw(canvas).text((60, 60), "meal tray close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_meal_close.png")

    canvas = render_base(data, bg_key="close_menu", front_layers=False)
    paste_center(canvas, PROPS / "menu_board_close.png", anchors["close_insert_center"], 0.82)
    ImageDraw.Draw(canvas).text((60, 60), "menu close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_menu_close.png")

    canvas = render_base(data, bg_key="close_counter", front_layers=False)
    paste_center(canvas, PROPS / "qr_code_close.png", anchors["close_insert_center"], 0.9)
    ImageDraw.Draw(canvas).text((60, 60), "QR payment close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_qr_close.png")

    save_contact_sheet(
        PREVIEWS / "takeout_shop_props_contact_sheet.png",
        [
            ("meal_tray_counter", PROPS / "meal_tray_counter.png"),
            ("meal_tray_hand", PROPS / "meal_tray_hand.png"),
            ("meal_tray_close", PROPS / "meal_tray_close.png"),
            ("noodle_bowl_table", PROPS / "noodle_bowl_table.png"),
            ("receipt_counter", PROPS / "receipt_counter.png"),
            ("receipt_hand", PROPS / "receipt_hand.png"),
            ("qr_code_counter", PROPS / "qr_code_counter.png"),
            ("qr_code_hand", PROPS / "qr_code_hand.png"),
            ("drink_counter", PROPS / "drink_counter.png"),
            ("delivery_bag_floor", PROPS / "delivery_bag_floor.png"),
            ("counter_bell", PROPS / "counter_bell_idle.png"),
            ("steam_puff", PROPS / "steam_puff.png"),
        ],
    )


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)

    draw_shop_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (420, 220, 1570, 920))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_counter.png", (560, 455, 1580, 945))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_kitchen.png", (700, 250, 1280, 635))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_menu.png", (1160, 30, 1860, 330))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_table.png", (65, 520, 600, 950))

    save_layer_counter(LAYERS / "counter_front.png")
    save_layer_shelf(LAYERS / "shelf_front.png")
    save_layer_door_frame(LAYERS / "kitchen_window_frame_front.png")

    save_meal_tray(PROPS / "meal_tray_counter.png")
    save_meal_tray(PROPS / "meal_tray_hand.png", hand=True)
    save_meal_tray(PROPS / "meal_tray_close.png", close=True)
    save_noodle_bowl(PROPS / "noodle_bowl_table.png")
    save_noodle_bowl(PROPS / "noodle_bowl_close.png", close=True)
    save_receipt(PROPS / "receipt_counter.png")
    save_receipt(PROPS / "receipt_hand.png", hand=True)
    save_receipt(PROPS / "receipt_close.png", close=True)
    save_qr_code(PROPS / "qr_code_counter.png")
    save_qr_code(PROPS / "qr_code_hand.png", hand=True)
    save_qr_code(PROPS / "qr_code_close.png", close=True)
    save_drink(PROPS / "drink_counter.png")
    save_drink(PROPS / "drink_hand.png", hand=True)
    save_delivery_bag(PROPS / "delivery_bag_floor.png")
    save_delivery_bag(PROPS / "delivery_bag_hand.png", hand=True)
    save_counter_bell(PROPS / "counter_bell_idle.png")
    save_menu_board(PROPS / "menu_board_close.png")
    save_steam(PROPS / "steam_puff.png")

    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
