from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_forest_path_01")
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


def draw_actor(draw: ImageDraw.ImageDraw, anchor: dict, label: str, color, fnt) -> None:
    x = int(anchor["x"] * SIZE[0])
    y = int(anchor["y"] * SIZE[1])
    scale = float(anchor.get("scale", 1))
    body_w = int(145 * scale)
    body_h = int(360 * scale)
    top = y - body_h
    left = x - body_w // 2
    draw.rounded_rectangle((left, top, left + body_w, y), radius=20, fill=color, outline=(18, 18, 20, 255), width=6)
    draw.ellipse((x - 45, top - 66, x + 45, top + 24), fill=(255, 224, 184, 255), outline=(18, 18, 20, 255), width=6)
    draw.text((left - 10, y + 8), label, fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def paste_center(canvas: Image.Image, path: Path, anchor: dict, scale: float = 1.0) -> None:
    img = Image.open(path).convert("RGBA")
    final = scale * float(anchor.get("scale", 1.0))
    w = max(1, int(img.width * final))
    h = max(1, int(img.height * final))
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(img, (int(anchor["x"] * SIZE[0] - w / 2), int(anchor["y"] * SIZE[1] - h / 2)))


def draw_forest_background(path: Path) -> None:
    img = rgba(color=(28, 46, 34, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(30, 50, 38, 255))
    d.rectangle((0, 0, 1920, 410), fill=(42, 70, 58, 255))
    for x in range(-120, 2100, 180):
        h = 360 + (x * 7) % 170
        d.rectangle((x + 74, 250, x + 108, 900), fill=(65, 43, 32, 255), outline=(32, 22, 18, 255), width=4)
        d.polygon([(x, 300), (x + 90, 80), (x + 190, 300)], fill=(28, 86, 45, 255), outline=(18, 48, 28, 255))
        d.polygon([(x - 20, 435), (x + 90, 160), (x + 210, 435)], fill=(24, 76, 39, 255), outline=(18, 48, 28, 255))
        d.polygon([(x - 40, 575), (x + 90, 250), (x + 230, 575)], fill=(20, 64, 34, 255), outline=(18, 48, 28, 255))
        d.rectangle((x + 80, 575, x + 102, min(900, h + 420)), fill=(66, 45, 34, 255))

    d.polygon([(0, 770), (1920, 770), (1920, 1080), (0, 1080)], fill=(42, 68, 42, 255))
    d.polygon([(500, 1080), (820, 720), (1110, 720), (1480, 1080)], fill=(120, 94, 60, 255), outline=(58, 42, 30, 255))
    for y in range(770, 1080, 70):
        d.arc((480, y - 40, 1440, y + 130), 8, 172, fill=(92, 70, 48, 255), width=4)
    d.ellipse((690, 570, 1230, 790), fill=(60, 90, 78, 120))
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS).save(target)


def save_layer_bush_front(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    for x in range(-80, 2000, 120):
        y = 860 + (x * 11) % 90
        d.ellipse((x, y, x + 210, y + 180), fill=(20, 74, 32, 230))
        d.ellipse((x + 50, y - 38, x + 190, y + 118), fill=(24, 88, 38, 230))
    img.save(path)


def save_layer_vines_front(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    for x in (240, 420, 1480, 1660):
        d.line((x, 0, x + 60, 520), fill=(34, 82, 38, 210), width=14)
        for y in range(100, 510, 95):
            d.ellipse((x + 20, y, x + 80, y + 38), fill=(42, 120, 52, 210))
    img.save(path)


def save_signpost(path: Path) -> None:
    img = rgba((360, 300))
    d = ImageDraw.Draw(img)
    d.rectangle((160, 112, 195, 285), fill=(92, 60, 38, 255), outline=(28, 22, 18, 255), width=5)
    d.polygon([(56, 42), (292, 42), (332, 92), (292, 142), (56, 142)], fill=(178, 116, 62, 255), outline=(28, 22, 18, 255))
    d.line((92, 82, 255, 82), fill=(42, 30, 24, 255), width=8)
    d.line((116, 112, 226, 112), fill=(42, 30, 24, 255), width=6)
    img.save(path)


def save_vine_trap(path: Path, hand: bool = False) -> None:
    img = rgba((420, 240))
    d = ImageDraw.Draw(img)
    for y in (92, 128, 164):
        d.arc((20, y - 80, 400, y + 90), 190, 350, fill=(42, 116, 48, 255), width=16)
        d.arc((35, y - 70, 385, y + 80), 190, 350, fill=(24, 70, 32, 255), width=5)
    for x in (90, 170, 250, 330):
        d.polygon([(x, 86), (x + 20, 122), (x - 12, 122)], fill=(50, 135, 58, 255), outline=(20, 52, 24, 255))
    if hand:
        d.rounded_rectangle((285, 30, 410, 100), radius=24, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_magic_barrier(path: Path) -> None:
    img = rgba((560, 560))
    d = ImageDraw.Draw(img)
    for i, color in enumerate(((80, 180, 220, 75), (80, 220, 170, 100), (230, 255, 220, 135))):
        inset = 42 + i * 44
        d.ellipse((inset, inset, 560 - inset, 560 - inset), outline=color, width=18)
    d.polygon([(280, 78), (430, 280), (280, 482), (130, 280)], outline=(215, 255, 230, 180), fill=(80, 220, 180, 44))
    img.save(path)


def save_dragon_head(path: Path, close: bool = False) -> None:
    img = rgba((720, 500) if close else (420, 300))
    d = ImageDraw.Draw(img)
    s = img.width / 420
    d.ellipse((72 * s, 82 * s, 338 * s, 250 * s), fill=(88, 150, 72, 255), outline=(18, 44, 24, 255), width=max(5, int(7 * s)))
    d.polygon([(78 * s, 112 * s), (22 * s, 48 * s), (130 * s, 78 * s)], fill=(70, 124, 62, 255), outline=(18, 44, 24, 255))
    d.polygon([(320 * s, 112 * s), (395 * s, 55 * s), (280 * s, 80 * s)], fill=(70, 124, 62, 255), outline=(18, 44, 24, 255))
    d.ellipse((130 * s, 130 * s, 178 * s, 178 * s), fill=(255, 220, 78, 255), outline=(18, 44, 24, 255), width=max(3, int(4 * s)))
    d.ellipse((244 * s, 130 * s, 292 * s, 178 * s), fill=(255, 220, 78, 255), outline=(18, 44, 24, 255), width=max(3, int(4 * s)))
    d.rectangle((152 * s, 152 * s, 160 * s, 176 * s), fill=(18, 44, 24, 255))
    d.rectangle((266 * s, 152 * s, 274 * s, 176 * s), fill=(18, 44, 24, 255))
    d.arc((138 * s, 172 * s, 284 * s, 240 * s), 10, 170, fill=(40, 68, 38, 255), width=max(4, int(5 * s)))
    d.polygon([(180 * s, 224 * s), (192 * s, 260 * s), (204 * s, 224 * s)], fill=(250, 250, 230, 255), outline=(18, 44, 24, 255))
    d.polygon([(238 * s, 224 * s), (250 * s, 260 * s), (262 * s, 224 * s)], fill=(250, 250, 230, 255), outline=(18, 44, 24, 255))
    img.save(path)


def save_qr_board(path: Path, hand: bool = False) -> None:
    img = rgba((300, 360))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((42, 32, 258, 315), radius=18, fill=(250, 250, 238, 255), outline=(28, 28, 28, 255), width=6)
    d.rectangle((80, 74, 220, 214), fill=(235, 235, 226, 255), outline=(28, 28, 28, 255), width=4)
    for y in range(88, 204, 28):
        for x in range(94, 210, 28):
            if (x + y) // 28 % 2 == 0:
                d.rectangle((x, y, x + 18, y + 18), fill=(30, 36, 34, 255))
    d.rounded_rectangle((85, 244, 215, 282), radius=10, fill=(92, 190, 100, 255), outline=(28, 28, 28, 255), width=3)
    if hand:
        d.rounded_rectangle((178, 3, 292, 66), radius=22, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_mushroom(path: Path) -> None:
    img = rgba((260, 220))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((108, 90, 154, 190), radius=20, fill=(246, 224, 180, 255), outline=(28, 28, 28, 255), width=5)
    d.pieslice((40, 35, 220, 145), 180, 360, fill=(210, 70, 80, 255), outline=(28, 28, 28, 255), width=6)
    for x, y in ((88, 82), (132, 60), (166, 92)):
        d.ellipse((x, y, x + 24, y + 24), fill=(255, 232, 206, 255), outline=(28, 28, 28, 255))
    img.save(path)


def save_fog_puff(path: Path) -> None:
    img = rgba((420, 210))
    d = ImageDraw.Draw(img)
    for x, y, w, h in ((20, 88, 160, 80), (110, 50, 190, 110), (250, 80, 150, 80)):
        d.ellipse((x, y, x + w, y + h), fill=(215, 230, 220, 120))
    img.save(path)


def save_delivery_map(path: Path, hand: bool = False) -> None:
    img = rgba((360, 260))
    d = ImageDraw.Draw(img)
    pts = [(42, 48), (300, 30), (330, 194), (72, 224)]
    d.polygon(pts, fill=(250, 235, 184, 255), outline=(28, 28, 28, 255))
    d.line((92, 92, 145, 132, 210, 98, 280, 166), fill=(210, 80, 68, 255), width=8)
    d.ellipse((200, 82, 232, 114), fill=(82, 170, 240, 255), outline=(28, 28, 28, 255), width=4)
    if hand:
        d.rounded_rectangle((4, 168, 118, 240), radius=24, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_contact_sheet(path: Path, assets: list[tuple[str, Path]]) -> None:
    thumb = (180, 150)
    margin = 24
    label_h = 30
    cols = 4
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb[0] + margin) + margin, rows * (thumb[1] + label_h + margin) + margin), (228, 232, 224))
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
        "scene_id": "scene_forest_path_01",
        "name": "诅咒森林道路交互样板",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_sign": "backgrounds/close_sign.png",
            "close_dragon": "backgrounds/close_dragon.png",
            "close_path": "backgrounds/close_path.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": ["layers/bush_front.png", "layers/vines_front.png"],
            "overlay": [],
        },
        "anchors": {
            "stand_left": {"x": 0.30, "y": 0.84, "scale": 0.86, "facing": "right"},
            "stand_right": {"x": 0.66, "y": 0.84, "scale": 0.86, "facing": "left"},
            "path_center": {"x": 0.50, "y": 0.78, "scale": 1.0},
            "signpost": {"x": 0.24, "y": 0.66, "scale": 1.0},
            "vine_trap": {"x": 0.52, "y": 0.73, "scale": 1.0},
            "barrier_center": {"x": 0.52, "y": 0.57, "scale": 1.0},
            "dragon_head": {"x": 0.73, "y": 0.48, "scale": 1.0},
            "qr_board": {"x": 0.58, "y": 0.56, "scale": 1.0},
            "mushroom_patch": {"x": 0.36, "y": 0.76, "scale": 1.0},
            "fog_center": {"x": 0.50, "y": 0.58, "scale": 1.0},
            "map_hand": {"x": 0.42, "y": 0.54, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
        },
        "props": {
            "signpost": {"label": "森林路牌", "variants": {"front": "props/signpost_front.png"}, "default_anchor": "signpost", "pivot": "center", "variant_scales": {"front": 0.82}},
            "vine_trap": {"label": "藤蔓陷阱", "variants": {"ground": "props/vine_trap_ground.png", "hand": "props/vine_trap_hand.png"}, "default_anchor": "vine_trap", "pivot": "center", "variant_scales": {"ground": 0.95, "hand": 0.7}},
            "magic_barrier": {"label": "魔法屏障", "variants": {"active": "props/magic_barrier_active.png"}, "default_anchor": "barrier_center", "pivot": "center", "variant_scales": {"active": 0.95}},
            "dragon": {"label": "巨龙", "variants": {"head": "props/dragon_head.png", "close": "props/dragon_head_close.png"}, "default_anchor": "dragon_head", "pivot": "center", "variant_scales": {"head": 0.88, "close": 1.0}},
            "qr_board": {"label": "扫码牌", "variants": {"table": "props/qr_board_table.png", "hand": "props/qr_board_hand.png"}, "default_anchor": "qr_board", "pivot": "center", "variant_scales": {"table": 0.72, "hand": 0.62}},
            "mushroom": {"label": "发光蘑菇", "variants": {"patch": "props/mushroom_patch.png"}, "default_anchor": "mushroom_patch", "pivot": "center", "variant_scales": {"patch": 0.82}},
            "fog": {"label": "迷雾", "variants": {"puff": "props/fog_puff.png"}, "default_anchor": "fog_center", "pivot": "center", "variant_scales": {"puff": 1.5}},
            "delivery_map": {"label": "配送地图", "variants": {"hand": "props/delivery_map_hand.png", "close": "props/delivery_map_close.png"}, "default_anchor": "map_hand", "pivot": "center", "variant_scales": {"hand": 0.72, "close": 0.96}},
        },
        "supported_actions": [
            "stand",
            "enter_forest",
            "read_sign",
            "clear_vines",
            "open_barrier",
            "encounter_dragon",
            "scan_qr",
            "check_map",
            "fog_reveal",
            "inspect_close",
        ],
        "action_templates": {
            "enter_forest": {"duration": 1.2, "actor_state_sequence": ["walk", "slow", "stand"], "target_anchor": "path_center"},
            "read_sign": {"duration": 1.2, "prop": "signpost", "prop_sequence": [{"time": 0.0, "variant": "front", "anchor": "signpost"}]},
            "clear_vines": {"duration": 1.3, "prop": "vine_trap", "prop_sequence": [{"time": 0.0, "variant": "ground", "anchor": "vine_trap"}, {"time": 0.8, "variant": "hand", "anchor": "actor.hand_r"}]},
            "open_barrier": {"duration": 1.0, "prop": "magic_barrier", "prop_sequence": [{"time": 0.0, "variant": "active", "anchor": "barrier_center", "motion": "pulse"}]},
            "encounter_dragon": {"duration": 1.5, "prop": "dragon", "prop_sequence": [{"time": 0.0, "variant": "head", "anchor": "dragon_head"}, {"time": 0.9, "variant": "close", "anchor": "close_insert_center"}]},
            "scan_qr": {"duration": 1.4, "prop": "qr_board", "prop_sequence": [{"time": 0.0, "variant": "table", "anchor": "qr_board"}, {"time": 0.7, "variant": "hand", "anchor": "actor.hand_r"}]},
            "check_map": {"duration": 1.2, "prop": "delivery_map", "prop_sequence": [{"time": 0.0, "variant": "hand", "anchor": "map_hand"}, {"time": 0.65, "variant": "close", "anchor": "close_insert_center"}]},
            "fog_reveal": {"duration": 1.0, "prop": "fog", "prop_sequence": [{"time": 0.0, "variant": "puff", "anchor": "fog_center", "motion": "fade"}]},
        },
    }


def render_base(data: dict, bg_key: str = "wide", front_layers: bool = True) -> Image.Image:
    canvas = Image.open(ROOT / data["backgrounds"][bg_key]).convert("RGBA")
    if front_layers:
        for rel in data["layers"]["front_character"]:
            canvas.alpha_composite(Image.open(ROOT / rel).convert("RGBA"))
    return canvas


def render_previews(data: dict) -> None:
    fnt = font(34)
    small = font(25)
    anchors = data["anchors"]
    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    for anchor_id, anchor in anchors.items():
        x = int(anchor["x"] * SIZE[0])
        y = int(anchor["y"] * SIZE[1])
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 90, 50, 255), outline=(0, 0, 0, 255), width=3)
        draw.text((x + 12, y - 22), anchor_id, fill=(255, 240, 180, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.alpha_composite(Image.open(LAYERS / "bush_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "vines_front.png").convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    for path, anchor_id, scale in [
        ("signpost_front.png", "signpost", 0.82),
        ("vine_trap_ground.png", "vine_trap", 0.95),
        ("magic_barrier_active.png", "barrier_center", 0.95),
        ("dragon_head.png", "dragon_head", 0.88),
        ("qr_board_table.png", "qr_board", 0.72),
        ("mushroom_patch.png", "mushroom_patch", 0.82),
        ("fog_puff.png", "fog_center", 1.5),
    ]:
        paste_center(canvas, PROPS / path, anchors[anchor_id], scale)
    canvas.alpha_composite(Image.open(LAYERS / "bush_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "forest path props", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "courier", (80, 145, 230, 255), fnt)
    paste_center(canvas, PROPS / "vine_trap_ground.png", anchors["vine_trap"], 0.95)
    paste_center(canvas, PROPS / "magic_barrier_active.png", anchors["barrier_center"], 0.95)
    canvas.alpha_composite(Image.open(LAYERS / "bush_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "clear_vines + open_barrier", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_obstacles.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "courier", (80, 145, 230, 255), fnt)
    paste_center(canvas, PROPS / "dragon_head.png", anchors["dragon_head"], 0.88)
    paste_center(canvas, PROPS / "qr_board_table.png", anchors["qr_board"], 0.72)
    ImageDraw.Draw(canvas).text((60, 60), "encounter_dragon + scan_qr", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_dragon_scan.png")

    canvas = render_base(data, bg_key="close_dragon", front_layers=False)
    paste_center(canvas, PROPS / "dragon_head_close.png", anchors["close_insert_center"], 1.0)
    ImageDraw.Draw(canvas).text((60, 60), "dragon close insert", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_dragon_close.png")

    canvas = render_base(data, bg_key="close_path", front_layers=False)
    paste_center(canvas, PROPS / "delivery_map_close.png", anchors["close_insert_center"], 0.96)
    ImageDraw.Draw(canvas).text((60, 60), "delivery map close insert", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_map_close.png")

    save_contact_sheet(PREVIEWS / "forest_path_props_contact_sheet.png", [
        ("signpost", PROPS / "signpost_front.png"),
        ("vine_ground", PROPS / "vine_trap_ground.png"),
        ("vine_hand", PROPS / "vine_trap_hand.png"),
        ("barrier", PROPS / "magic_barrier_active.png"),
        ("dragon_head", PROPS / "dragon_head.png"),
        ("dragon_close", PROPS / "dragon_head_close.png"),
        ("qr_board", PROPS / "qr_board_table.png"),
        ("qr_hand", PROPS / "qr_board_hand.png"),
        ("mushroom", PROPS / "mushroom_patch.png"),
        ("fog", PROPS / "fog_puff.png"),
        ("map_hand", PROPS / "delivery_map_hand.png"),
        ("map_close", PROPS / "delivery_map_close.png"),
    ])


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)
    draw_forest_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (350, 250, 1570, 900))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_sign.png", (180, 310, 760, 760))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_dragon.png", (930, 200, 1710, 850))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_path.png", (560, 560, 1370, 980))
    save_layer_bush_front(LAYERS / "bush_front.png")
    save_layer_vines_front(LAYERS / "vines_front.png")
    save_signpost(PROPS / "signpost_front.png")
    save_vine_trap(PROPS / "vine_trap_ground.png")
    save_vine_trap(PROPS / "vine_trap_hand.png", hand=True)
    save_magic_barrier(PROPS / "magic_barrier_active.png")
    save_dragon_head(PROPS / "dragon_head.png")
    save_dragon_head(PROPS / "dragon_head_close.png", close=True)
    save_qr_board(PROPS / "qr_board_table.png")
    save_qr_board(PROPS / "qr_board_hand.png", hand=True)
    save_mushroom(PROPS / "mushroom_patch.png")
    save_fog_puff(PROPS / "fog_puff.png")
    save_delivery_map(PROPS / "delivery_map_hand.png", hand=True)
    save_delivery_map(PROPS / "delivery_map_close.png")
    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
