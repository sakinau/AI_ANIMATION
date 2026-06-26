from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_fantasy_market_01")
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
    body_w = int(142 * scale)
    body_h = int(350 * scale)
    top = y - body_h
    left = x - body_w // 2
    draw.rounded_rectangle((left, top, left + body_w, y), radius=20, fill=color, outline=(18, 18, 20, 255), width=6)
    draw.ellipse((x - 45, top - 64, x + 45, top + 24), fill=(255, 224, 184, 255), outline=(18, 18, 20, 255), width=6)
    draw.text((left - 8, y + 8), label, fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def draw_market_background(path: Path) -> None:
    img = rgba(color=(218, 207, 178, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(222, 210, 184, 255))
    d.rectangle((0, 0, 1920, 460), fill=(154, 200, 222, 255))
    d.ellipse((-160, 110, 270, 470), fill=(116, 158, 106, 255), outline=(72, 112, 76, 255), width=6)
    d.ellipse((1640, 90, 2070, 460), fill=(116, 158, 106, 255), outline=(72, 112, 76, 255), width=6)
    d.rectangle((0, 460, 1920, 720), fill=(176, 146, 104, 255))
    d.rectangle((0, 720, 1920, 1080), fill=(122, 104, 82, 255))
    for y in range(770, 1080, 82):
        d.line((0, y, 1920, y), fill=(92, 78, 64, 255), width=5)
    for x in range(-120, 2100, 230):
        d.line((x, 720, x + 170, 1080), fill=(92, 78, 64, 255), width=5)

    # Buildings.
    for x, w, h, roof in ((150, 350, 300, (166, 78, 66, 255)), (610, 410, 340, (96, 118, 160, 255)), (1320, 390, 310, (166, 78, 66, 255))):
        d.rectangle((x, 420 - h // 2, x + w, 650), fill=(198, 166, 118, 255), outline=(58, 46, 36, 255), width=7)
        d.polygon([(x - 35, 420 - h // 2), (x + w // 2, 250 - h // 2), (x + w + 35, 420 - h // 2)], fill=roof, outline=(58, 46, 36, 255))
        d.rectangle((x + 50, 515, x + 150, 650), fill=(86, 64, 50, 255), outline=(58, 46, 36, 255), width=5)
        d.rectangle((x + w - 150, 470, x + w - 55, 560), fill=(130, 190, 215, 255), outline=(58, 46, 36, 255), width=5)

    # Stalls and fountain.
    d.rounded_rectangle((150, 580, 620, 820), radius=18, fill=(142, 88, 54, 255), outline=(45, 32, 24, 255), width=7)
    d.polygon([(120, 575), (650, 575), (590, 455), (180, 455)], fill=(220, 80, 70, 255), outline=(45, 32, 24, 255))
    for x in range(180, 595, 70):
        d.polygon([(x, 455), (x + 35, 575), (x + 70, 455)], fill=(245, 212, 120, 255), outline=(45, 32, 24, 255))
    d.rounded_rectangle((1290, 590, 1775, 825), radius=18, fill=(122, 86, 58, 255), outline=(45, 32, 24, 255), width=7)
    d.polygon([(1265, 585), (1805, 585), (1745, 465), (1325, 465)], fill=(82, 136, 174, 255), outline=(45, 32, 24, 255))
    for x in range(1325, 1745, 70):
        d.polygon([(x, 465), (x + 35, 585), (x + 70, 465)], fill=(235, 224, 150, 255), outline=(45, 32, 24, 255))
    d.ellipse((820, 580, 1110, 725), fill=(102, 150, 174, 255), outline=(45, 54, 60, 255), width=8)
    d.rectangle((882, 498, 1048, 650), fill=(128, 162, 176, 255), outline=(45, 54, 60, 255), width=7)
    d.ellipse((870, 455, 1060, 535), fill=(168, 212, 224, 255), outline=(45, 54, 60, 255), width=7)
    for x in (900, 965, 1030):
        d.line((x, 460, x - 42, 585), fill=(190, 230, 240, 165), width=8)

    # Notice board and signpost.
    d.rounded_rectangle((705, 565, 815, 735), radius=10, fill=(116, 78, 52, 255), outline=(45, 32, 24, 255), width=6)
    d.rectangle((718, 592, 802, 690), fill=(244, 224, 158, 255), outline=(45, 32, 24, 255), width=4)
    d.rectangle((1150, 520, 1176, 785), fill=(86, 62, 42, 255))
    d.polygon([(1160, 540), (1300, 575), (1160, 610)], fill=(244, 196, 82, 255), outline=(45, 32, 24, 255))
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS).save(target)


def save_layer_left_stall(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((150, 670, 620, 842), radius=18, fill=(142, 88, 54, 255), outline=(45, 32, 24, 255), width=7)
    img.save(path)


def save_layer_right_stall(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1290, 680, 1775, 846), radius=18, fill=(122, 86, 58, 255), outline=(45, 32, 24, 255), width=7)
    img.save(path)


def save_layer_fountain(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.ellipse((820, 645, 1110, 755), fill=(88, 136, 160, 255), outline=(45, 54, 60, 255), width=7)
    img.save(path)


def save_coin_pouch(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((430, 360) if close else (230, 190))
    d = ImageDraw.Draw(img)
    s = img.width / 230
    d.ellipse((52 * s, 58 * s, 178 * s, 172 * s), fill=(126, 78, 52, 255), outline=(30, 24, 22, 255), width=max(4, int(5 * s)))
    d.rectangle((72 * s, 40 * s, 158 * s, 82 * s), fill=(168, 102, 64, 255), outline=(30, 24, 22, 255), width=max(3, int(4 * s)))
    d.ellipse((92 * s, 92 * s, 140 * s, 140 * s), fill=(238, 202, 76, 255), outline=(30, 24, 22, 255), width=max(3, int(4 * s)))
    if hand:
        d.rounded_rectangle((138 * s, 18 * s, 226 * s, 82 * s), radius=int(20 * s), fill=(255, 220, 178, 255), outline=(30, 24, 22, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_potion(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((360, 520) if close else (190, 280))
    d = ImageDraw.Draw(img)
    s = img.width / 190
    d.rectangle((78 * s, 24 * s, 112 * s, 70 * s), fill=(230, 210, 170, 255), outline=(24, 24, 24, 255), width=max(3, int(4 * s)))
    d.rounded_rectangle((45 * s, 65 * s, 145 * s, 240 * s), radius=int(34 * s), fill=(170, 80, 210, 225), outline=(24, 24, 24, 255), width=max(4, int(5 * s)))
    d.ellipse((62 * s, 110 * s, 128 * s, 175 * s), fill=(226, 150, 255, 185))
    if hand:
        d.rounded_rectangle((98 * s, 36 * s, 188 * s, 104 * s), radius=int(22 * s), fill=(255, 220, 178, 255), outline=(24, 24, 24, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_apple_crate(path: Path, hand: bool = False) -> None:
    img = rgba((330, 260))
    d = ImageDraw.Draw(img)
    d.rectangle((46, 110, 288, 230), fill=(164, 100, 58, 255), outline=(42, 30, 24, 255), width=6)
    for x in (78, 134, 190, 246):
        d.ellipse((x, 52, x + 58, 112), fill=(220, 62, 56, 255), outline=(42, 30, 24, 255), width=4)
        d.line((x + 30, 55, x + 42, 35), fill=(58, 90, 48, 255), width=4)
    if hand:
        d.rounded_rectangle((218, 38, 326, 102), radius=22, fill=(255, 220, 178, 255), outline=(42, 30, 24, 255), width=5)
    img.save(path)


def save_notice(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((520, 640) if close else (240, 300))
    d = ImageDraw.Draw(img)
    s = img.width / 240
    d.rounded_rectangle((28 * s, 18 * s, 212 * s, 275 * s), radius=int(10 * s), fill=(246, 226, 158, 255), outline=(45, 32, 24, 255), width=max(4, int(5 * s)))
    d.polygon([(96 * s, 48 * s), (128 * s, 118 * s), (64 * s, 118 * s)], fill=(230, 80, 70, 255), outline=(45, 32, 24, 255))
    for y, w in ((145, 112), (178, 138), (212, 86)):
        d.rectangle((58 * s, y * s, (58 + w) * s, (y + 10) * s), fill=(64, 52, 42, 255))
    if hand:
        d.rounded_rectangle((140 * s, 18 * s, 238 * s, 88 * s), radius=int(22 * s), fill=(255, 220, 178, 255), outline=(45, 32, 24, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_map_scroll(path: Path, hand: bool = False, close: bool = False) -> None:
    img = rgba((580, 430) if close else (300, 210))
    d = ImageDraw.Draw(img)
    s = img.width / 300
    d.rounded_rectangle((35 * s, 42 * s, 265 * s, 168 * s), radius=int(14 * s), fill=(250, 232, 174, 255), outline=(48, 36, 28, 255), width=max(4, int(5 * s)))
    d.line((72 * s, 130 * s, 128 * s, 78 * s, 180 * s, 118 * s, 232 * s, 72 * s), fill=(88, 132, 86, 255), width=max(3, int(5 * s)))
    d.ellipse((205 * s, 58 * s, 226 * s, 78 * s), fill=(220, 68, 58, 255))
    if hand:
        d.rounded_rectangle((198 * s, 22 * s, 296 * s, 86 * s), radius=int(22 * s), fill=(255, 220, 178, 255), outline=(48, 36, 28, 255), width=max(3, int(5 * s)))
    img.save(path)


def save_signpost(path: Path) -> None:
    img = rgba((360, 360))
    d = ImageDraw.Draw(img)
    d.rectangle((168, 70, 194, 330), fill=(86, 62, 42, 255), outline=(42, 30, 24, 255), width=4)
    d.polygon([(178, 78), (324, 112), (178, 148)], fill=(244, 196, 82, 255), outline=(42, 30, 24, 255))
    d.polygon([(184, 168), (46, 204), (184, 238)], fill=(244, 196, 82, 255), outline=(42, 30, 24, 255))
    d.rectangle((205, 105, 280, 118), fill=(58, 42, 32, 255))
    d.rectangle((80, 196, 150, 208), fill=(58, 42, 32, 255))
    img.save(path)


def save_reaction_mark(path: Path) -> None:
    img = rgba((280, 260))
    d = ImageDraw.Draw(img)
    d.polygon([(140, 20), (178, 132), (252, 72), (196, 160), (260, 214), (156, 186), (112, 246), (102, 170), (22, 188), (88, 122), (48, 50)], fill=(255, 222, 66, 255), outline=(40, 34, 28, 255))
    d.rectangle((132, 78, 150, 166), fill=(40, 34, 28, 255))
    d.ellipse((126, 180, 156, 210), fill=(40, 34, 28, 255))
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
        "scene_id": "scene_fantasy_market_01",
        "name": "fantasy market square interaction pack",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_left_stall": "backgrounds/close_left_stall.png",
            "close_right_stall": "backgrounds/close_right_stall.png",
            "close_notice": "backgrounds/close_notice.png",
            "close_fountain": "backgrounds/close_fountain.png",
            "close_signpost": "backgrounds/close_signpost.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": ["layers/left_stall_front.png", "layers/right_stall_front.png", "layers/fountain_front.png"],
            "overlay": [],
        },
        "anchors": {
            "stand_left": {"x": 0.30, "y": 0.84, "scale": 0.84, "facing": "right"},
            "stand_center": {"x": 0.50, "y": 0.84, "scale": 0.84, "facing": "front"},
            "stand_right": {"x": 0.70, "y": 0.84, "scale": 0.84, "facing": "left"},
            "vendor_left": {"x": 0.23, "y": 0.75, "scale": 0.74, "facing": "right"},
            "vendor_right": {"x": 0.78, "y": 0.75, "scale": 0.74, "facing": "left"},
            "left_stall_counter": {"x": 0.20, "y": 0.62, "scale": 1.0},
            "right_stall_counter": {"x": 0.78, "y": 0.62, "scale": 1.0},
            "notice_board": {"x": 0.40, "y": 0.59, "scale": 1.0},
            "fountain_center": {"x": 0.50, "y": 0.62, "scale": 1.0},
            "signpost": {"x": 0.61, "y": 0.58, "scale": 1.0},
            "coin_handoff": {"x": 0.31, "y": 0.58, "scale": 1.0},
            "potion_handoff": {"x": 0.70, "y": 0.58, "scale": 1.0},
            "map_hand": {"x": 0.50, "y": 0.53, "scale": 1.0},
            "reaction_top": {"x": 0.50, "y": 0.24, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
        },
        "props": {
            "coin_pouch": {
                "label": "coin pouch",
                "variants": {"table": "props/coin_pouch_table.png", "hand": "props/coin_pouch_hand.png", "close": "props/coin_pouch_close.png"},
                "default_anchor": "coin_handoff",
                "pivot": "center",
                "variant_scales": {"table": 0.62, "hand": 0.56, "close": 1.0},
            },
            "potion": {
                "label": "magic potion",
                "variants": {"table": "props/potion_table.png", "hand": "props/potion_hand.png", "close": "props/potion_close.png"},
                "default_anchor": "right_stall_counter",
                "pivot": "center",
                "variant_scales": {"table": 0.62, "hand": 0.56, "close": 0.95},
            },
            "apple_crate": {
                "label": "apple crate",
                "variants": {"table": "props/apple_crate_table.png", "hand": "props/apple_crate_hand.png"},
                "default_anchor": "left_stall_counter",
                "pivot": "center",
                "variant_scales": {"table": 0.78, "hand": 0.58},
            },
            "notice": {
                "label": "quest notice",
                "variants": {"board": "props/notice_board.png", "hand": "props/notice_hand.png", "close": "props/notice_close.png"},
                "default_anchor": "notice_board",
                "pivot": "center",
                "variant_scales": {"board": 0.62, "hand": 0.54, "close": 0.95},
            },
            "map_scroll": {
                "label": "route map",
                "variants": {"hand": "props/map_scroll_hand.png", "close": "props/map_scroll_close.png"},
                "default_anchor": "map_hand",
                "pivot": "center",
                "variant_scales": {"hand": 0.58, "close": 0.95},
            },
            "signpost": {
                "label": "direction signpost",
                "variants": {"front": "props/signpost_front.png"},
                "default_anchor": "signpost",
                "pivot": "center",
                "variant_scales": {"front": 0.86},
            },
            "reaction_mark": {
                "label": "crowd reaction",
                "variants": {"shock": "props/reaction_shock.png"},
                "default_anchor": "reaction_top",
                "pivot": "center",
                "variant_scales": {"shock": 0.72},
            },
        },
        "supported_actions": [
            "stand",
            "enter_market",
            "trade_coin",
            "buy_potion",
            "buy_food",
            "read_notice",
            "take_notice",
            "check_map",
            "ask_directions",
            "gather_at_fountain",
            "crowd_reaction",
            "inspect_close",
        ],
        "action_templates": {
            "enter_market": {"duration": 1.0, "actor_state_sequence": ["offscreen", "walk", "stand"], "target_anchor": "stand_center"},
            "trade_coin": {
                "duration": 1.1,
                "prop": "coin_pouch",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "actor.hand_r"},
                    {"time": 0.7, "variant": "table", "anchor": "left_stall_counter"},
                ],
            },
            "buy_potion": {
                "duration": 1.2,
                "prop": "potion",
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "right_stall_counter"},
                    {"time": 0.7, "variant": "hand", "anchor": "actor.hand_l"},
                ],
            },
            "buy_food": {
                "duration": 1.0,
                "prop": "apple_crate",
                "prop_sequence": [
                    {"time": 0.0, "variant": "table", "anchor": "left_stall_counter"},
                    {"time": 0.65, "variant": "hand", "anchor": "actor.hand_r"},
                ],
            },
            "read_notice": {
                "duration": 1.1,
                "prop": "notice",
                "prop_sequence": [
                    {"time": 0.0, "variant": "board", "anchor": "notice_board"},
                    {"time": 0.6, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "take_notice": {
                "duration": 1.0,
                "prop": "notice",
                "prop_sequence": [
                    {"time": 0.0, "variant": "board", "anchor": "notice_board"},
                    {"time": 0.55, "variant": "hand", "anchor": "actor.hand_r"},
                ],
            },
            "check_map": {
                "duration": 1.1,
                "prop": "map_scroll",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "map_hand"},
                    {"time": 0.6, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "ask_directions": {
                "duration": 0.9,
                "prop": "signpost",
                "prop_sequence": [{"time": 0.0, "variant": "front", "anchor": "signpost"}],
            },
            "gather_at_fountain": {"duration": 1.2, "target_anchor": "fountain_center", "requires_front_layers": ["fountain_front"]},
            "crowd_reaction": {
                "duration": 0.7,
                "prop": "reaction_mark",
                "prop_sequence": [{"time": 0.0, "variant": "shock", "anchor": "reaction_top", "motion": "pop_in"}],
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
    for layer in ("left_stall_front.png", "right_stall_front.png", "fountain_front.png"):
        canvas.alpha_composite(Image.open(LAYERS / layer).convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "apple_crate_table.png", anchors["left_stall_counter"], 0.78)
    paste_center(canvas, PROPS / "coin_pouch_table.png", anchors["coin_handoff"], 0.62)
    paste_center(canvas, PROPS / "potion_table.png", anchors["right_stall_counter"], 0.62)
    paste_center(canvas, PROPS / "notice_board.png", anchors["notice_board"], 0.62)
    paste_center(canvas, PROPS / "signpost_front.png", anchors["signpost"], 0.86)
    canvas.alpha_composite(Image.open(LAYERS / "left_stall_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "right_stall_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "fantasy market props", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "courier", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["vendor_left"], "vendor", (210, 92, 72, 255), fnt)
    paste_center(canvas, PROPS / "coin_pouch_hand.png", anchors["coin_handoff"], 0.56)
    paste_center(canvas, PROPS / "apple_crate_table.png", anchors["left_stall_counter"], 0.78)
    canvas.alpha_composite(Image.open(LAYERS / "left_stall_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "trade_coin / buy_food", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_trade_left.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_right"], "courier", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["vendor_right"], "alchemist", (142, 94, 190, 255), fnt)
    paste_center(canvas, PROPS / "potion_hand.png", anchors["potion_handoff"], 0.56)
    canvas.alpha_composite(Image.open(LAYERS / "right_stall_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "buy_potion", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_buy_potion.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_center"], "courier", (80, 145, 230, 255), fnt)
    paste_center(canvas, PROPS / "notice_close.png", anchors["close_insert_center"], 0.95)
    paste_center(canvas, PROPS / "reaction_shock.png", anchors["reaction_top"], 0.72)
    ImageDraw.Draw(canvas).text((60, 60), "read_notice + reaction", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_notice_reaction.png")

    canvas = render_base(data, bg_key="close_fountain", front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "party", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["stand_right"], "guide", (210, 92, 72, 255), fnt)
    paste_center(canvas, PROPS / "map_scroll_hand.png", anchors["map_hand"], 0.58)
    ImageDraw.Draw(canvas).text((60, 60), "fountain meeting + map", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_fountain_map.png")

    canvas = render_base(data, bg_key="close_notice", front_layers=False)
    paste_center(canvas, PROPS / "notice_close.png", anchors["close_insert_center"], 0.95)
    ImageDraw.Draw(canvas).text((60, 60), "notice close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_notice_close.png")

    canvas = render_base(data, bg_key="close_signpost", front_layers=False)
    paste_center(canvas, PROPS / "signpost_front.png", anchors["close_insert_center"], 0.86)
    ImageDraw.Draw(canvas).text((60, 60), "signpost close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_signpost_close.png")

    save_contact_sheet(
        PREVIEWS / "fantasy_market_props_contact_sheet.png",
        [
            ("coin_pouch_table", PROPS / "coin_pouch_table.png"),
            ("coin_pouch_hand", PROPS / "coin_pouch_hand.png"),
            ("potion_table", PROPS / "potion_table.png"),
            ("potion_hand", PROPS / "potion_hand.png"),
            ("apple_crate", PROPS / "apple_crate_table.png"),
            ("apple_hand", PROPS / "apple_crate_hand.png"),
            ("notice_board", PROPS / "notice_board.png"),
            ("notice_hand", PROPS / "notice_hand.png"),
            ("map_scroll_hand", PROPS / "map_scroll_hand.png"),
            ("signpost", PROPS / "signpost_front.png"),
            ("reaction_shock", PROPS / "reaction_shock.png"),
        ],
    )


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)

    draw_market_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (360, 290, 1560, 920))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_left_stall.png", (70, 390, 720, 860))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_right_stall.png", (1190, 400, 1840, 870))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_notice.png", (640, 500, 900, 790))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_fountain.png", (720, 420, 1210, 800))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_signpost.png", (1050, 450, 1360, 800))

    save_layer_left_stall(LAYERS / "left_stall_front.png")
    save_layer_right_stall(LAYERS / "right_stall_front.png")
    save_layer_fountain(LAYERS / "fountain_front.png")

    save_coin_pouch(PROPS / "coin_pouch_table.png")
    save_coin_pouch(PROPS / "coin_pouch_hand.png", hand=True)
    save_coin_pouch(PROPS / "coin_pouch_close.png", close=True)
    save_potion(PROPS / "potion_table.png")
    save_potion(PROPS / "potion_hand.png", hand=True)
    save_potion(PROPS / "potion_close.png", close=True)
    save_apple_crate(PROPS / "apple_crate_table.png")
    save_apple_crate(PROPS / "apple_crate_hand.png", hand=True)
    save_notice(PROPS / "notice_board.png")
    save_notice(PROPS / "notice_hand.png", hand=True)
    save_notice(PROPS / "notice_close.png", close=True)
    save_map_scroll(PROPS / "map_scroll_hand.png", hand=True)
    save_map_scroll(PROPS / "map_scroll_close.png", close=True)
    save_signpost(PROPS / "signpost_front.png")
    save_reaction_mark(PROPS / "reaction_shock.png")

    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
