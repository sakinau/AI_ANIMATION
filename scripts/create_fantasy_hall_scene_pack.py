from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_fantasy_hall_01")
BACKGROUNDS = ROOT / "backgrounds"
LAYERS = ROOT / "layers"
PROPS = ROOT / "props"
PREVIEWS = ROOT / "previews"

SIZE = (1920, 1080)


def rgba(size=SIZE, color=(0, 0, 0, 0)) -> Image.Image:
    return Image.new("RGBA", size, color)


def load_font(size: int):
    for name in ("msyh.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_actor(draw: ImageDraw.ImageDraw, anchor: dict, label: str, color: tuple[int, int, int, int], font) -> None:
    x = int(anchor["x"] * SIZE[0])
    y = int(anchor["y"] * SIZE[1])
    scale = float(anchor.get("scale", 1))
    body_w = int(150 * scale)
    body_h = int(390 * scale)
    top = y - body_h
    left = x - body_w // 2
    draw.rounded_rectangle((left, top, left + body_w, y), radius=22, fill=color, outline=(18, 18, 20, 255), width=6)
    draw.ellipse((x - 48, top - 70, x + 48, top + 26), fill=(255, 224, 184, 255), outline=(18, 18, 20, 255), width=6)
    draw.text((left - 16, y + 10), label, fill=(255, 245, 180, 255), font=font, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def paste_center(canvas: Image.Image, path: Path, anchor: dict, scale: float = 1.0) -> None:
    img = Image.open(path).convert("RGBA")
    final_scale = scale * float(anchor.get("scale", 1.0))
    w = max(1, int(img.width * final_scale))
    h = max(1, int(img.height * final_scale))
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    x = int(anchor["x"] * SIZE[0] - w / 2)
    y = int(anchor["y"] * SIZE[1] - h / 2)
    canvas.alpha_composite(img, (x, y))


def draw_hall_background(path: Path) -> None:
    img = rgba(color=(44, 38, 54, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(42, 34, 52, 255))
    for i in range(9):
        y = 110 + i * 90
        shade = 48 + i * 5
        d.rectangle((0, y, 1920, y + 72), fill=(shade, shade - 8, shade + 8, 255))
        d.line((0, y, 1920, y), fill=(20, 18, 24, 255), width=4)

    d.polygon([(0, 760), (1920, 760), (1920, 1080), (0, 1080)], fill=(74, 64, 76, 255))
    for x in range(-200, 2100, 220):
        d.line((x, 760, x + 260, 1080), fill=(44, 38, 48, 255), width=5)
    for y in range(820, 1080, 80):
        d.line((0, y, 1920, y), fill=(50, 45, 54, 255), width=4)

    # Pillars and torch windows.
    for x in (185, 455, 1465, 1735):
        d.rounded_rectangle((x, 180, x + 90, 810), radius=18, fill=(92, 82, 96, 255), outline=(24, 22, 28, 255), width=7)
        d.rectangle((x - 18, 160, x + 108, 212), fill=(117, 105, 122, 255), outline=(24, 22, 28, 255), width=6)
        d.rectangle((x - 26, 790, x + 116, 842), fill=(72, 62, 76, 255), outline=(24, 22, 28, 255), width=6)
    for x in (340, 1550):
        d.rounded_rectangle((x, 285, x + 150, 540), radius=44, fill=(28, 20, 34, 255), outline=(18, 16, 20, 255), width=8)
        d.polygon([(x + 30, 510), (x + 75, 330), (x + 120, 510)], fill=(244, 94, 52, 255))
        d.polygon([(x + 48, 500), (x + 75, 375), (x + 102, 500)], fill=(255, 212, 82, 255))

    # Distant throne silhouette and carpet.
    d.polygon([(760, 790), (1160, 790), (1240, 1080), (680, 1080)], fill=(104, 35, 48, 255), outline=(36, 16, 22, 255))
    d.rounded_rectangle((780, 350, 1140, 800), radius=30, fill=(92, 55, 100, 255), outline=(22, 18, 26, 255), width=8)
    d.polygon([(820, 350), (960, 210), (1100, 350)], fill=(132, 82, 142, 255), outline=(22, 18, 26, 255))
    d.ellipse((925, 250, 995, 320), fill=(245, 203, 80, 255), outline=(22, 18, 26, 255), width=5)
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    img = Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS)
    img.save(target)


def save_layer_throne_front(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((760, 640, 1160, 880), radius=26, fill=(73, 43, 84, 210), outline=(28, 20, 34, 255), width=8)
    d.rectangle((705, 830, 1215, 910), fill=(56, 38, 66, 220), outline=(26, 20, 30, 255), width=7)
    img.save(path)


def save_layer_table_front(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((515, 662, 1405, 890), radius=26, fill=(92, 58, 38, 215), outline=(34, 23, 18, 255), width=8)
    d.rectangle((545, 635, 1375, 705), fill=(123, 78, 46, 230), outline=(34, 23, 18, 255), width=7)
    d.rectangle((620, 880, 720, 1035), fill=(70, 46, 36, 230), outline=(34, 23, 18, 255), width=6)
    d.rectangle((1200, 880, 1300, 1035), fill=(70, 46, 36, 230), outline=(34, 23, 18, 255), width=6)
    img.save(path)


def save_layer_portal_frame(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.ellipse((1285, 250, 1785, 900), outline=(98, 52, 150, 210), width=32)
    d.ellipse((1325, 295, 1745, 860), outline=(220, 100, 255, 170), width=16)
    img.save(path)


def save_meal_box(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((520, 420) if close else (260, 210))
    d = ImageDraw.Draw(img)
    s = img.width / 260
    d.rounded_rectangle((32 * s, 70 * s, 232 * s, 185 * s), radius=int(18 * s), fill=(250, 150, 56, 255), outline=(24, 24, 28, 255), width=max(4, int(6 * s)))
    d.polygon([(32 * s, 70 * s), (86 * s, 24 * s), (206 * s, 24 * s), (232 * s, 70 * s)], fill=(255, 190, 74, 255), outline=(24, 24, 28, 255))
    d.rounded_rectangle((88 * s, 102 * s, 178 * s, 145 * s), radius=int(10 * s), fill=(255, 245, 218, 255), outline=(24, 24, 28, 255), width=max(3, int(4 * s)))
    d.line((104 * s, 120 * s, 164 * s, 120 * s), fill=(220, 75, 52, 255), width=max(3, int(4 * s)))
    if hand:
        d.rounded_rectangle((175 * s, 20 * s, 256 * s, 78 * s), radius=int(20 * s), fill=(255, 220, 178, 255), outline=(24, 24, 28, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_magic_scroll(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((560, 420) if close else (260, 180))
    d = ImageDraw.Draw(img)
    s = img.width / 260
    d.rounded_rectangle((32 * s, 35 * s, 220 * s, 145 * s), radius=int(12 * s), fill=(255, 235, 178, 255), outline=(37, 26, 22, 255), width=max(4, int(5 * s)))
    for y in (64, 88, 112):
        d.line((64 * s, y * s, 190 * s, (y - 8) * s), fill=(90, 60, 80, 255), width=max(2, int(3 * s)))
    d.line((76 * s, 128 * s, 155 * s, 116 * s), fill=(210, 60, 80, 255), width=max(3, int(4 * s)))
    d.ellipse((20 * s, 42 * s, 58 * s, 140 * s), fill=(220, 182, 128, 255), outline=(37, 26, 22, 255), width=max(3, int(4 * s)))
    if hand:
        d.rounded_rectangle((2 * s, 108 * s, 85 * s, 172 * s), radius=int(18 * s), fill=(255, 220, 178, 255), outline=(24, 24, 28, 255), width=max(4, int(5 * s)))
    img.save(path)


def save_coin(path: Path, hand: bool = False) -> None:
    img = rgba((200, 160))
    d = ImageDraw.Draw(img)
    d.ellipse((38, 28, 132, 122), fill=(245, 205, 70, 255), outline=(24, 24, 28, 255), width=6)
    d.ellipse((58, 48, 112, 102), outline=(194, 135, 42, 255), width=5)
    d.rectangle((82, 54, 90, 96), fill=(194, 135, 42, 255))
    if hand:
        d.rounded_rectangle((95, 12, 196, 76), radius=22, fill=(255, 220, 178, 255), outline=(24, 24, 28, 255), width=5)
    img.save(path)


def save_portal(path: Path) -> None:
    img = rgba((480, 620))
    d = ImageDraw.Draw(img)
    for i, color in enumerate(((88, 42, 130, 130), (158, 68, 210, 160), (240, 125, 255, 190))):
        inset = i * 34
        d.ellipse((inset, inset, 480 - inset, 620 - inset), fill=color, outline=(245, 210, 255, 180), width=8)
    for x in range(90, 390, 70):
        d.arc((x - 80, 110, x + 110, 520), 250, 80, fill=(255, 255, 255, 95), width=5)
    img.save(path)


def save_magic_warning(path: Path) -> None:
    img = rgba((620, 330))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 602, 312), radius=28, fill=(40, 20, 52, 245), outline=(234, 80, 155, 255), width=8)
    d.polygon([(82, 74), (140, 205), (24, 205)], fill=(255, 205, 65, 255), outline=(24, 24, 28, 255))
    d.rectangle((78, 110, 88, 168), fill=(24, 24, 28, 255))
    d.ellipse((72, 180, 94, 202), fill=(24, 24, 28, 255))
    for y, w in ((82, 360), (138, 430), (194, 300)):
        d.rounded_rectangle((180, y, 180 + w, y + 26), radius=8, fill=(246, 230, 250, 255))
    img.save(path)


def save_sword(path: Path, hand: bool = False) -> None:
    img = rgba((300, 260))
    d = ImageDraw.Draw(img)
    d.polygon([(152, 18), (182, 138), (152, 220), (122, 138)], fill=(220, 232, 238, 255), outline=(24, 24, 28, 255))
    d.rectangle((82, 138, 222, 160), fill=(190, 145, 60, 255), outline=(24, 24, 28, 255))
    d.rectangle((140, 155, 164, 246), fill=(82, 52, 42, 255), outline=(24, 24, 28, 255))
    if hand:
        d.rounded_rectangle((166, 165, 288, 226), radius=22, fill=(255, 220, 178, 255), outline=(24, 24, 28, 255), width=5)
    img.save(path)


def save_contact_sheet(output_path: Path, assets: list[tuple[str, Path]]) -> None:
    thumb = (180, 150)
    margin = 24
    label_h = 30
    cols = 4
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb[0] + margin) + margin, rows * (thumb[1] + label_h + margin) + margin), (230, 224, 218))
    d = ImageDraw.Draw(sheet)
    font = load_font(15)
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
        d.text((x, y + thumb[1] + 8), label, fill=(20, 20, 20), font=font)
    sheet.save(output_path)


def build_scene_yaml() -> dict:
    return {
        "scene_id": "scene_fantasy_hall_01",
        "name": "魔王城大厅交互样板",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_throne": "backgrounds/close_throne.png",
            "close_portal": "backgrounds/close_portal.png",
            "close_table": "backgrounds/close_table.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": [
                "layers/throne_front.png",
                "layers/table_front.png",
                "layers/portal_frame_front.png",
            ],
            "overlay": [],
        },
        "anchors": {
            "stand_left": {"x": 0.28, "y": 0.83, "scale": 0.86, "facing": "right"},
            "stand_right": {"x": 0.66, "y": 0.83, "scale": 0.88, "facing": "left"},
            "throne_sit": {"x": 0.50, "y": 0.77, "scale": 0.94, "facing": "front"},
            "table_center": {"x": 0.50, "y": 0.61, "scale": 1.0},
            "table_meal": {"x": 0.45, "y": 0.56, "scale": 1.0},
            "table_scroll": {"x": 0.56, "y": 0.55, "scale": 1.0},
            "table_coin": {"x": 0.64, "y": 0.57, "scale": 1.0},
            "portal_entry": {"x": 0.80, "y": 0.82, "scale": 0.84, "facing": "left"},
            "portal_center": {"x": 0.80, "y": 0.52, "scale": 1.0},
            "handoff_mid": {"x": 0.47, "y": 0.55, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "warning_center": {"x": 0.50, "y": 0.32, "scale": 1.0},
            "weapon_rack": {"x": 0.22, "y": 0.62, "scale": 1.0},
        },
        "props": {
            "meal_box": {
                "label": "外卖盒",
                "variants": {
                    "table": "props/meal_box_table.png",
                    "hand": "props/meal_box_hand.png",
                    "close": "props/meal_box_close.png",
                },
                "default_anchor": "table_meal",
                "pivot": "center",
                "variant_scales": {"table": 0.72, "hand": 0.55, "close": 1.0},
            },
            "magic_scroll": {
                "label": "魔法订单",
                "variants": {
                    "table": "props/magic_scroll_table.png",
                    "hand": "props/magic_scroll_hand.png",
                    "close": "props/magic_scroll_close.png",
                },
                "default_anchor": "table_scroll",
                "pivot": "center",
                "variant_scales": {"table": 0.68, "hand": 0.58, "close": 0.95},
            },
            "coin": {
                "label": "金币",
                "variants": {"table": "props/coin_table.png", "hand": "props/coin_hand.png"},
                "default_anchor": "table_coin",
                "pivot": "center",
                "variant_scales": {"table": 0.7, "hand": 0.65},
            },
            "portal": {
                "label": "传送门",
                "variants": {"open": "props/portal_open.png"},
                "default_anchor": "portal_center",
                "pivot": "center",
                "variant_scales": {"open": 1.05},
            },
            "magic_warning": {
                "label": "魔法警告",
                "variants": {"warning": "props/magic_warning.png"},
                "default_anchor": "warning_center",
                "pivot": "center",
                "variant_scales": {"warning": 0.82},
            },
            "sword": {
                "label": "短剑",
                "variants": {"table": "props/sword_table.png", "hand": "props/sword_hand.png"},
                "default_anchor": "weapon_rack",
                "pivot": "center",
                "variant_scales": {"table": 0.72, "hand": 0.66},
            },
        },
        "supported_actions": [
            "stand",
            "sit_throne",
            "enter_from_portal",
            "deliver_meal",
            "read_magic_order",
            "hand_over_coin",
            "open_portal",
            "show_magic_warning",
            "inspect_close",
            "draw_sword",
        ],
        "action_templates": {
            "sit_throne": {
                "duration": 1.0,
                "actor_state_sequence": ["stand", "turn", "sit"],
                "target_anchor": "throne_sit",
                "requires_front_layers": ["throne_front"],
            },
            "enter_from_portal": {
                "duration": 1.3,
                "actor_state_sequence": ["offscreen", "step_out", "stand"],
                "from_anchor": "portal_entry",
                "requires_front_layers": ["portal_frame_front"],
            },
            "deliver_meal": {
                "duration": 1.4,
                "actor_state_sequence": ["carry", "extend", "release"],
                "prop": "meal_box",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "actor.hand_r"},
                    {"time": 0.85, "variant": "table", "anchor": "table_meal"},
                ],
            },
            "read_magic_order": {
                "duration": 1.5,
                "actor_state_sequence": ["reach", "hold", "read"],
                "prop": "magic_scroll",
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "table_scroll"},
                    {"time": 0.65, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "hand_over_coin": {
                "duration": 1.1,
                "prop": "coin",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "actor.hand_r"},
                    {"time": 0.7, "variant": "table", "anchor": "table_coin"},
                ],
            },
            "open_portal": {
                "duration": 1.0,
                "prop": "portal",
                "prop_sequence": [{"time": 0.0, "variant": "open", "anchor": "portal_center"}],
            },
            "show_magic_warning": {
                "duration": 1.0,
                "prop": "magic_warning",
                "prop_sequence": [{"time": 0.0, "variant": "warning", "anchor": "warning_center", "motion": "pop_in"}],
            },
            "draw_sword": {
                "duration": 1.0,
                "prop": "sword",
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "weapon_rack"},
                    {"time": 0.65, "variant": "hand", "anchor": "actor.hand_r"},
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
    font = load_font(34)
    small = load_font(26)
    anchors = data["anchors"]

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    for anchor_id, anchor in anchors.items():
        x = int(anchor["x"] * SIZE[0])
        y = int(anchor["y"] * SIZE[1])
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 90, 50, 255), outline=(0, 0, 0, 255), width=3)
        draw.text((x + 12, y - 22), anchor_id, fill=(255, 240, 180, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.alpha_composite(Image.open(LAYERS / "throne_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "table_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "portal_frame_front.png").convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "portal_open.png", anchors["portal_center"], 1.05)
    paste_center(canvas, PROPS / "meal_box_table.png", anchors["table_meal"], 0.72)
    paste_center(canvas, PROPS / "magic_scroll_table.png", anchors["table_scroll"], 0.68)
    paste_center(canvas, PROPS / "coin_table.png", anchors["table_coin"], 0.7)
    paste_center(canvas, PROPS / "sword_table.png", anchors["weapon_rack"], 0.72)
    canvas.alpha_composite(Image.open(LAYERS / "table_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "portal_frame_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "fantasy hall props", fill=(255, 245, 180, 255), font=font, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "courier", (80, 145, 230, 255), font)
    draw_actor(draw, anchors["throne_sit"], "demon king", (170, 80, 190, 255), font)
    paste_center(canvas, PROPS / "meal_box_hand.png", anchors["handoff_mid"], 0.55)
    canvas.alpha_composite(Image.open(LAYERS / "throne_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "table_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "deliver_meal / handoff", fill=(255, 245, 180, 255), font=font, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_deliver_meal.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "portal_open.png", anchors["portal_center"], 1.08)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["portal_entry"], "enter", (80, 145, 230, 255), font)
    paste_center(canvas, PROPS / "magic_warning.png", anchors["warning_center"], 0.82)
    canvas.alpha_composite(Image.open(LAYERS / "portal_frame_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "enter_from_portal + warning", fill=(255, 245, 180, 255), font=font, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_portal_warning.png")

    canvas = render_base(data, bg_key="close_table", front_layers=False)
    paste_center(canvas, PROPS / "magic_scroll_close.png", anchors["close_insert_center"], 0.95)
    ImageDraw.Draw(canvas).text((60, 60), "read_magic_order close insert", fill=(255, 245, 180, 255), font=font, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_magic_order_close.png")

    assets = [
        ("meal_box_table", PROPS / "meal_box_table.png"),
        ("meal_box_hand", PROPS / "meal_box_hand.png"),
        ("meal_box_close", PROPS / "meal_box_close.png"),
        ("magic_scroll_table", PROPS / "magic_scroll_table.png"),
        ("magic_scroll_hand", PROPS / "magic_scroll_hand.png"),
        ("magic_scroll_close", PROPS / "magic_scroll_close.png"),
        ("coin_table", PROPS / "coin_table.png"),
        ("coin_hand", PROPS / "coin_hand.png"),
        ("portal_open", PROPS / "portal_open.png"),
        ("magic_warning", PROPS / "magic_warning.png"),
        ("sword_table", PROPS / "sword_table.png"),
        ("sword_hand", PROPS / "sword_hand.png"),
    ]
    save_contact_sheet(PREVIEWS / "fantasy_hall_props_contact_sheet.png", assets)


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)

    draw_hall_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (360, 160, 1560, 835))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_throne.png", (650, 180, 1270, 890))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_portal.png", (1180, 200, 1880, 930))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_table.png", (470, 470, 1430, 930))

    save_layer_throne_front(LAYERS / "throne_front.png")
    save_layer_table_front(LAYERS / "table_front.png")
    save_layer_portal_frame(LAYERS / "portal_frame_front.png")

    save_meal_box(PROPS / "meal_box_table.png")
    save_meal_box(PROPS / "meal_box_hand.png", hand=True)
    save_meal_box(PROPS / "meal_box_close.png", close=True)
    save_magic_scroll(PROPS / "magic_scroll_table.png")
    save_magic_scroll(PROPS / "magic_scroll_hand.png", hand=True)
    save_magic_scroll(PROPS / "magic_scroll_close.png", close=True)
    save_coin(PROPS / "coin_table.png")
    save_coin(PROPS / "coin_hand.png", hand=True)
    save_portal(PROPS / "portal_open.png")
    save_magic_warning(PROPS / "magic_warning.png")
    save_sword(PROPS / "sword_table.png")
    save_sword(PROPS / "sword_hand.png", hand=True)

    data = build_scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
